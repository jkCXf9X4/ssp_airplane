from __future__ import annotations

import ctypes
import socket
import sys
import threading
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.lib.artifacts.build.native import build_flightgear_bridge_fmu  # type: ignore  # noqa: E402


class CallbackFunctions(ctypes.Structure):
    _fields_ = [
        ("logger", ctypes.c_void_p),
        ("allocateMemory", ctypes.c_void_p),
        ("freeMemory", ctypes.c_void_p),
        ("stepFinished", ctypes.c_void_p),
        ("componentEnvironment", ctypes.c_void_p),
    ]


def _free_udp_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def _extract_fmu(fmu_path: Path, target: Path) -> tuple[Path, ET.ElementTree]:
    with zipfile.ZipFile(fmu_path) as archive:
        archive.extractall(target)
    tree = ET.parse(target / "modelDescription.xml")
    return target / "binaries" / "linux64" / "FlightGearBridge.so", tree


def _value_refs(tree: ET.ElementTree) -> dict[str, int]:
    refs: dict[str, int] = {}
    for scalar in tree.iterfind(".//ScalarVariable"):
        refs[scalar.attrib["name"]] = int(scalar.attrib["valueReference"])
    return refs


def _load_library(path: Path) -> ctypes.CDLL:
    lib = ctypes.CDLL(str(path))
    lib.fmi2Instantiate.restype = ctypes.c_void_p
    lib.fmi2Instantiate.argtypes = [
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_char_p,
        ctypes.POINTER(CallbackFunctions),
        ctypes.c_int,
        ctypes.c_int,
    ]
    lib.fmi2SetupExperiment.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.c_double,
        ctypes.c_double,
        ctypes.c_int,
        ctypes.c_double,
    ]
    lib.fmi2EnterInitializationMode.argtypes = [ctypes.c_void_p]
    lib.fmi2ExitInitializationMode.argtypes = [ctypes.c_void_p]
    lib.fmi2SetReal.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double),
    ]
    lib.fmi2SetInteger.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_int),
    ]
    lib.fmi2SetBoolean.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_int),
    ]
    lib.fmi2SetString.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_char_p),
    ]
    lib.fmi2DoStep.argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_double, ctypes.c_int]
    lib.fmi2GetReal.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_double),
    ]
    lib.fmi2GetInteger.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_int),
    ]
    lib.fmi2Terminate.argtypes = [ctypes.c_void_p]
    lib.fmi2FreeInstance.argtypes = [ctypes.c_void_p]
    return lib


def test_native_flightgear_bridge_fmu_exchanges_udp_packets(tmp_path: Path):
    telemetry_port = _free_udp_port()
    control_port = _free_udp_port()
    fmu_path = build_flightgear_bridge_fmu(
        output_fmu=tmp_path / "FlightGearBridge.fmu",
        build_dir=tmp_path / "native_build",
    )

    extract_dir = tmp_path / "extracted"
    library_path, model_description = _extract_fmu(fmu_path, extract_dir)
    refs = _value_refs(model_description)
    guid = model_description.getroot().attrib["guid"]

    received_packets: list[str] = []
    telemetry_ready = threading.Event()

    def telemetry_listener() -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("127.0.0.1", telemetry_port))
        sock.settimeout(3.0)
        telemetry_ready.set()
        payload, _ = sock.recvfrom(4096)
        received_packets.append(payload.decode().strip())
        sock.close()

    listener = threading.Thread(target=telemetry_listener, daemon=True)
    listener.start()
    telemetry_ready.wait(timeout=1.0)

    lib = _load_library(library_path)
    callbacks = CallbackFunctions()
    component = lib.fmi2Instantiate(
        b"bridge-test",
        1,
        guid.encode(),
        None,
        ctypes.byref(callbacks),
        0,
        0,
    )
    assert component

    try:
        assert lib.fmi2SetupExperiment(component, 0, 0.0, 0.0, 0, 0.0) == 0
        assert lib.fmi2EnterInitializationMode(component) == 0

        string_refs = (ctypes.c_uint * 1)(refs["remote_host"])
        string_values = (ctypes.c_char_p * 1)(b"127.0.0.1")
        assert lib.fmi2SetString(component, string_refs, 1, string_values) == 0

        int_refs = (ctypes.c_uint * 2)(refs["telemetry_port"], refs["control_port"])
        int_values = (ctypes.c_int * 2)(telemetry_port, control_port)
        assert lib.fmi2SetInteger(component, int_refs, 2, int_values) == 0

        real_pairs = [
            ("reference_latitude_deg", 57.700000),
            ("reference_longitude_deg", 11.950000),
            ("reference_altitude_m", 12.0),
            ("statePosition.x_km", 11.1),
            ("statePosition.y_km", 5.55),
            ("statePosition.z_km", 1.25),
            ("stateOrientation.roll_deg", 2.0),
            ("stateOrientation.pitch_deg", 3.0),
            ("stateOrientation.yaw_deg", 91.0),
            ("flightStatus.airspeed_mps", 250.0),
            ("flightStatus.energy_state_norm", 0.8),
            ("flightStatus.angle_of_attack_deg", 4.5),
            ("flightStatus.climb_rate", 12.0),
            ("missionStatus.distance_to_waypoint_km", 42.0),
        ]
        real_refs = (ctypes.c_uint * len(real_pairs))(*(refs[name] for name, _ in real_pairs))
        real_values = (ctypes.c_double * len(real_pairs))(*(value for _, value in real_pairs))
        assert lib.fmi2SetReal(component, real_refs, len(real_pairs), real_values) == 0

        mission_int_refs = (ctypes.c_uint * 3)(
            refs["flightStatus.health_code"],
            refs["missionStatus.waypoint_index"],
            refs["missionStatus.total_waypoints"],
        )
        mission_int_values = (ctypes.c_int * 3)(2, 3, 9)
        assert lib.fmi2SetInteger(component, mission_int_refs, 3, mission_int_values) == 0

        mission_bool_refs = (ctypes.c_uint * 2)(refs["missionStatus.arrived"], refs["missionStatus.complete"])
        mission_bool_values = (ctypes.c_int * 2)(1, 0)
        assert lib.fmi2SetBoolean(component, mission_bool_refs, 2, mission_bool_values) == 0

        assert lib.fmi2ExitInitializationMode(component) in (0, 1)

        control_sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        control_sender.sendto(
            b"0.250000,-0.500000,0.100000,0.800000,0.820000,7,1,-1,3,9\n",
            ("127.0.0.1", control_port),
        )
        control_sender.close()

        assert lib.fmi2DoStep(component, 0.0, 0.1, 1) == 0

        listener.join(timeout=3.0)
        assert received_packets, "Expected telemetry packet from native bridge FMU"

        telemetry_fields = received_packets[0].split(",")
        assert len(telemetry_fields) == 16
        assert abs(float(telemetry_fields[0]) - 57.8) < 0.01
        assert abs(float(telemetry_fields[1]) - 12.044) < 0.02
        assert abs(float(telemetry_fields[2]) - 4140.419) < 0.5
        assert abs(float(telemetry_fields[6]) - 485.961) < 0.5
        assert int(telemetry_fields[11]) == 3
        assert int(telemetry_fields[12]) == 9

        output_real_refs = (ctypes.c_uint * 5)(
            refs["pilotCommand.stick_pitch_norm"],
            refs["pilotCommand.stick_roll_norm"],
            refs["pilotCommand.rudder_norm"],
            refs["pilotCommand.throttle_norm"],
            refs["pilotCommand.throttle_aux_norm"],
        )
        output_real_values = (ctypes.c_double * 5)()
        assert lib.fmi2GetReal(component, output_real_refs, 5, output_real_values) == 0
        assert [round(value, 3) for value in output_real_values] == [0.25, -0.5, 0.1, 0.8, 0.82]

        output_int_refs = (ctypes.c_uint * 5)(
            refs["pilotCommand.button_mask"],
            refs["pilotCommand.hat_x"],
            refs["pilotCommand.hat_y"],
            refs["pilotCommand.mode_switch"],
            refs["pilotCommand.reserved"],
        )
        output_int_values = (ctypes.c_int * 5)()
        assert lib.fmi2GetInteger(component, output_int_refs, 5, output_int_values) == 0
        assert list(output_int_values) == [7, 1, -1, 3, 9]
    finally:
        lib.fmi2Terminate(component)
        lib.fmi2FreeInstance(component)
