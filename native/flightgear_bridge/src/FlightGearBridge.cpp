#include <cstring>

#include "BridgeRuntime.hpp"

namespace {

inline fgbridge::ModelInstance* as_instance(fmi2Component component) { return reinterpret_cast<fgbridge::ModelInstance*>(component); }

const Aircraft_FieldBinding* find_binding(fmi2ValueReference value_reference, Aircraft_ScalarType scalar_type) {
  for (size_t i = 0; i < Aircraft_FlightGearBridge_BindingCount; ++i) {
    const auto& binding = Aircraft_FlightGearBridge_Bindings[i];
    if (binding.value_reference == static_cast<int>(value_reference) && binding.scalar_type == scalar_type) {
      return &binding;
    }
  }
  return nullptr;
}

template <typename T>
T* binding_ptr(fgbridge::ModelInstance* instance, const Aircraft_FieldBinding& binding) {
  return reinterpret_cast<T*>(reinterpret_cast<char*>(instance) + binding.offset);
}

template <typename T>
const T* binding_ptr(const fgbridge::ModelInstance* instance, const Aircraft_FieldBinding& binding) {
  return reinterpret_cast<const T*>(reinterpret_cast<const char*>(instance) + binding.offset);
}

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
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_REAL);
    if (binding == nullptr) {
      return fmi2Error;
    }
    value[i] = *binding_ptr<double>(instance, *binding);
  }
  return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_INTEGER);
    if (binding == nullptr) {
      return fmi2Error;
    }
    value[i] = *binding_ptr<int>(instance, *binding);
  }
  return fmi2OK;
}

fmi2Status fmi2GetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_BOOLEAN);
    if (binding == nullptr) {
      return fmi2Error;
    }
    value[i] = static_cast<fmi2Boolean>(*binding_ptr<bool>(instance, *binding));
  }
  return fmi2OK;
}

fmi2Status fmi2GetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_STRING);
    if (binding == nullptr) {
      return fmi2Error;
    }
    value[i] = binding_ptr<std::string>(instance, *binding)->c_str();
  }
  return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_REAL);
    if (binding == nullptr || !binding->writable) {
      return fmi2Error;
    }
    *binding_ptr<double>(instance, *binding) = value[i];
  }
  return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_INTEGER);
    if (binding == nullptr || !binding->writable) {
      return fmi2Error;
    }
    *binding_ptr<int>(instance, *binding) = value[i];
    network_param_changed = network_param_changed
        || vr[i] == AIRCRAFT_FLIGHTGEARBRIDGE_VR_TELEMETRY_PORT
        || vr[i] == AIRCRAFT_FLIGHTGEARBRIDGE_VR_CONTROL_PORT;
  }
  if (network_param_changed) {
    fgbridge::invalidate_network(instance);
  }
  return fmi2OK;
}

fmi2Status fmi2SetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Boolean value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_BOOLEAN);
    if (binding == nullptr || !binding->writable) {
      return fmi2Error;
    }
    *binding_ptr<bool>(instance, *binding) = value[i] != fmi2False;
  }
  return fmi2OK;
}

fmi2Status fmi2SetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    const auto* binding = find_binding(vr[i], AIRCRAFT_SCALAR_STRING);
    if (binding == nullptr || !binding->writable) {
      return fmi2Error;
    }
    *binding_ptr<std::string>(instance, *binding) = value[i] ? value[i] : "";
    network_param_changed = network_param_changed || vr[i] == AIRCRAFT_FLIGHTGEARBRIDGE_VR_REMOTE_HOST;
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
