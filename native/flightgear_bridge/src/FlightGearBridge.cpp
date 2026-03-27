#include <cstring>

#include "BridgeRuntime.hpp"

namespace {

inline fgbridge::ModelInstance* as_instance(fmi2Component component) { return reinterpret_cast<fgbridge::ModelInstance*>(component); }

}  // namespace

extern "C" {

const char* fmi2GetTypesPlatform() { return fgbridge::kTypesPlatform; }

const char* fmi2GetVersion() { return fgbridge::kVersion; }

fmi2Status fmi2SetDebugLogging(fmi2Component, fmi2Boolean, size_t, const fmi2String[]) { return fmi2OK; }

fmi2Component fmi2Instantiate(
    fmi2String,
    fmi2Type fmuType,
    fmi2String fmuGUID,
    fmi2String,
    const fmi2CallbackFunctions*,
    fmi2Boolean,
    fmi2Boolean) {
  if (fmuType != fmi2CoSimulation) {
    return nullptr;
  }
  if (fmuGUID == nullptr || std::strcmp(fmuGUID, fgbridge::kGuid) != 0) {
    return nullptr;
  }
  return reinterpret_cast<fmi2Component>(fgbridge::create_instance());
}

void fmi2FreeInstance(fmi2Component component) { fgbridge::destroy_instance(as_instance(component)); }

fmi2Status fmi2SetupExperiment(
    fmi2Component,
    fmi2Boolean,
    fmi2Real,
    fmi2Real,
    fmi2Boolean,
    fmi2Real) {
  return fmi2OK;
}

fmi2Status fmi2EnterInitializationMode(fmi2Component) { return fmi2OK; }

fmi2Status fmi2ExitInitializationMode(fmi2Component component) { return fgbridge::enter_initialization(as_instance(component)); }

fmi2Status fmi2Terminate(fmi2Component component) { return fgbridge::reset_instance(as_instance(component)); }

fmi2Status fmi2Reset(fmi2Component component) { return fgbridge::reset_instance(as_instance(component)); }

fmi2Status fmi2GetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG: value[i] = instance->reference_latitude_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG: value[i] = instance->reference_longitude_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M: value[i] = instance->reference_altitude_m; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM: value[i] = instance->statePosition.x_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM: value[i] = instance->statePosition.y_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM: value[i] = instance->statePosition.z_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG: value[i] = instance->stateOrientation.roll_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG: value[i] = instance->stateOrientation.pitch_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG: value[i] = instance->stateOrientation.yaw_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS: value[i] = instance->flightStatus.airspeed_mps; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM: value[i] = instance->flightStatus.energy_state_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG: value[i] = instance->flightStatus.angle_of_attack_deg; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE: value[i] = instance->flightStatus.climb_rate; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM: value[i] = instance->missionStatus.distance_to_waypoint_km; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_PITCH_NORM: value[i] = instance->pilotCommand.stick_pitch_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_STICK_ROLL_NORM: value[i] = instance->pilotCommand.stick_roll_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RUDDER_NORM: value[i] = instance->pilotCommand.rudder_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_NORM: value[i] = instance->pilotCommand.throttle_norm; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_THROTTLE_AUX_NORM: value[i] = instance->pilotCommand.throttle_aux_norm; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT: value[i] = instance->telemetry_port; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT: value[i] = instance->control_port; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE: value[i] = instance->flightStatus.health_code; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX: value[i] = instance->missionStatus.waypoint_index; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS: value[i] = instance->missionStatus.total_waypoints; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK: value[i] = instance->pilotCommand.button_mask; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X: value[i] = instance->pilotCommand.hat_x; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y: value[i] = instance->pilotCommand.hat_y; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH: value[i] = instance->pilotCommand.mode_switch; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED: value[i] = instance->pilotCommand.reserved; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED: value[i] = static_cast<fmi2Boolean>(instance->missionStatus.arrived); break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE: value[i] = static_cast<fmi2Boolean>(instance->missionStatus.complete); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2GetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT: value[i] = instance->transport.c_str(); break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST: value[i] = instance->remote_host.c_str(); break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LATITUDE_DEG: instance->reference_latitude_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_LONGITUDE_DEG: instance->reference_longitude_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REFERENCE_ALTITUDE_M: instance->reference_altitude_m = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_X_KM: instance->statePosition.x_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Y_KM: instance->statePosition.y_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEPOSITION_Z_KM: instance->statePosition.z_km = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_ROLL_DEG: instance->stateOrientation.roll_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_PITCH_DEG: instance->stateOrientation.pitch_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_STATEORIENTATION_YAW_DEG: instance->stateOrientation.yaw_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_AIRSPEED_MPS: instance->flightStatus.airspeed_mps = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ENERGY_STATE_NORM: instance->flightStatus.energy_state_norm = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_ANGLE_OF_ATTACK_DEG: instance->flightStatus.angle_of_attack_deg = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_CLIMB_RATE: instance->flightStatus.climb_rate = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_DISTANCE_TO_WAYPOINT_KM: instance->missionStatus.distance_to_waypoint_km = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT: instance->telemetry_port = value[i]; network_param_changed = true; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT: instance->control_port = value[i]; network_param_changed = true; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_FLIGHTSTATUS_HEALTH_CODE: instance->flightStatus.health_code = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_WAYPOINT_INDEX: instance->missionStatus.waypoint_index = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_TOTAL_WAYPOINTS: instance->missionStatus.total_waypoints = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_BUTTON_MASK: instance->pilotCommand.button_mask = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_X: instance->pilotCommand.hat_x = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_HAT_Y: instance->pilotCommand.hat_y = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_MODE_SWITCH: instance->pilotCommand.mode_switch = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_PILOTCOMMAND_RESERVED: instance->pilotCommand.reserved = value[i]; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    fgbridge::invalidate_network(instance);
  }
  return fmi2OK;
}

fmi2Status fmi2SetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_ARRIVED: instance->missionStatus.arrived = value[i]; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_MISSIONSTATUS_COMPLETE: instance->missionStatus.complete = value[i]; break;
      default: return fmi2Error;
    }
  }
  return fmi2OK;
}

fmi2Status fmi2SetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    switch (vr[i]) {
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_TRANSPORT: instance->transport = value[i] ? value[i] : ""; break;
      case AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST: instance->remote_host = value[i] ? value[i] : ""; network_param_changed = true; break;
      default: return fmi2Error;
    }
  }
  if (network_param_changed) {
    fgbridge::invalidate_network(instance);
  }
  return fmi2OK;
}

fmi2Status fmi2DoStep(fmi2Component component, fmi2Real, fmi2Real, fmi2Boolean) { return fgbridge::do_step(as_instance(component)); }

fmi2Status fmi2CancelStep(fmi2Component) { return fmi2OK; }

fmi2Status fmi2GetStatus(fmi2Component, const fmi2StatusKind, fmi2Status* value) {
  if (value != nullptr) {
    *value = fmi2OK;
  }
  return fmi2OK;
}

fmi2Status fmi2GetRealStatus(fmi2Component, const fmi2StatusKind, fmi2Real* value) {
  if (value != nullptr) {
    *value = 0.0;
  }
  return fmi2OK;
}

fmi2Status fmi2GetIntegerStatus(fmi2Component, const fmi2StatusKind, fmi2Integer* value) { if (value != nullptr) { *value = 0; } return fmi2OK; }

fmi2Status fmi2GetBooleanStatus(fmi2Component, const fmi2StatusKind, fmi2Boolean* value) { if (value != nullptr) { *value = fmi2False; } return fmi2OK; }

fmi2Status fmi2GetStringStatus(fmi2Component, const fmi2StatusKind, fmi2String* value) { if (value != nullptr) { *value = ""; } return fmi2OK; }

fmi2Status fmi2SetRealInputDerivatives(fmi2Component, const fmi2ValueReference[], size_t, const fmi2Integer[], const fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetRealOutputDerivatives(fmi2Component, const fmi2ValueReference[], size_t, const fmi2Integer[], fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetDirectionalDerivative(fmi2Component, const fmi2ValueReference[], size_t, const fmi2ValueReference[], size_t, const fmi2Real[], fmi2Real[]) {
  return fmi2Error;
}

fmi2Status fmi2GetFMUstate(fmi2Component, fmi2FMUstate*) {
  return fmi2Error;
}

fmi2Status fmi2SetFMUstate(fmi2Component, fmi2FMUstate) {
  return fmi2Error;
}

fmi2Status fmi2FreeFMUstate(fmi2Component, fmi2FMUstate*) {
  return fmi2Error;
}

fmi2Status fmi2SerializedFMUstateSize(fmi2Component, fmi2FMUstate, size_t*) {
  return fmi2Error;
}

fmi2Status fmi2SerializeFMUstate(fmi2Component, fmi2FMUstate, fmi2Byte[], size_t) {
  return fmi2Error;
}

fmi2Status fmi2DeSerializeFMUstate(fmi2Component, const fmi2Byte[], size_t, fmi2FMUstate*) {
  return fmi2Error;
}

}  // extern "C"
