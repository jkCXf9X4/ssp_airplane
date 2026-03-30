#include <cstring>

#include "BridgeRuntime.hpp"

namespace {

inline fgbridge::ModelInstance* as_instance(fmi2Component component) { return reinterpret_cast<fgbridge::ModelInstance*>(component); }

inline const Aircraft_VrMapping* lookup_mapping(const fgbridge::ModelInstance* instance, fmi2ValueReference vr) {
  return vr < Aircraft_FlightGearBridge_VrCount ? &instance->vr_map[vr] : nullptr;
}

inline Aircraft_VrMapping* lookup_mapping(fgbridge::ModelInstance* instance, fmi2ValueReference vr) {
  return vr < Aircraft_FlightGearBridge_VrCount ? &instance->vr_map[vr] : nullptr;
}

template <typename T>
inline T* mapping_ptr(Aircraft_VrMapping* mapping) {
  return static_cast<T*>(mapping->data);
}

template <typename T>
inline const T* mapping_ptr(const Aircraft_VrMapping* mapping) {
  return static_cast<const T*>(mapping->data);
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

fmi2Status fmi2EnterInitializationMode(fmi2Component component) {
  Aircraft_FlightGearBridge_initialize_vr_map(as_instance(component));
  return fmi2OK;
}

fmi2Status fmi2ExitInitializationMode(fmi2Component component) { return fgbridge::enter_initialization(as_instance(component)); }

fmi2Status fmi2Terminate(fmi2Component component) { return fgbridge::reset_instance(as_instance(component)); }

fmi2Status fmi2Reset(fmi2Component component) {
  auto* instance = as_instance(component);
  auto status = fgbridge::reset_instance(instance);
  Aircraft_FlightGearBridge_initialize_vr_map(instance);
  return status;
}

fmi2Status fmi2GetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Real value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_REAL || mapping->data == nullptr) {
      return fmi2Error;
    }
    value[i] = *mapping_ptr<double>(mapping);
  }
  return fmi2OK;
}

fmi2Status fmi2GetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Integer value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_INTEGER || mapping->data == nullptr) {
      return fmi2Error;
    }
    value[i] = *mapping_ptr<int>(mapping);
  }
  return fmi2OK;
}

fmi2Status fmi2GetBoolean(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2Boolean value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_BOOLEAN || mapping->data == nullptr) {
      return fmi2Error;
    }
    value[i] = static_cast<fmi2Boolean>(*mapping_ptr<bool>(mapping));
  }
  return fmi2OK;
}

fmi2Status fmi2GetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, fmi2String value[]) {
  const auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    const auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_STRING || mapping->data == nullptr) {
      return fmi2Error;
    }
    value[i] = mapping_ptr<std::string>(mapping)->c_str();
  }
  return fmi2OK;
}

fmi2Status fmi2SetReal(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Real value[]) {
  auto* instance = as_instance(component);
  for (size_t i = 0; i < nvr; ++i) {
    auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_REAL || mapping->data == nullptr || !mapping->writable) {
      return fmi2Error;
    }
    *mapping_ptr<double>(mapping) = value[i];
  }
  return fmi2OK;
}

fmi2Status fmi2SetInteger(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2Integer value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_INTEGER || mapping->data == nullptr || !mapping->writable) {
      return fmi2Error;
    }
    *mapping_ptr<int>(mapping) = value[i];
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
    auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_BOOLEAN || mapping->data == nullptr || !mapping->writable) {
      return fmi2Error;
    }
    *mapping_ptr<bool>(mapping) = value[i] != fmi2False;
  }
  return fmi2OK;
}

fmi2Status fmi2SetString(fmi2Component component, const fmi2ValueReference vr[], size_t nvr, const fmi2String value[]) {
  auto* instance = as_instance(component);
  bool network_param_changed = false;
  for (size_t i = 0; i < nvr; ++i) {
    auto* mapping = lookup_mapping(instance, vr[i]);
    if (mapping == nullptr || mapping->type != AIRCRAFT_DATA_STRING || mapping->data == nullptr || !mapping->writable) {
      return fmi2Error;
    }
    *mapping_ptr<std::string>(mapping) = value[i] ? value[i] : "";
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

fmi2Status fmi2GetFMUstate(fmi2Component, fmi2FMUstate*) { return fmi2Error; }

fmi2Status fmi2SetFMUstate(fmi2Component, fmi2FMUstate) { return fmi2Error; }

fmi2Status fmi2FreeFMUstate(fmi2Component, fmi2FMUstate*) { return fmi2Error; }

fmi2Status fmi2SerializedFMUstateSize(fmi2Component, fmi2FMUstate, size_t*) { return fmi2Error; }

fmi2Status fmi2SerializeFMUstate(fmi2Component, fmi2FMUstate, fmi2Byte[], size_t) { return fmi2Error; }

fmi2Status fmi2DeSerializeFMUstate(fmi2Component, const fmi2Byte[], size_t, fmi2FMUstate*) { return fmi2Error; }

}  // extern "C"
