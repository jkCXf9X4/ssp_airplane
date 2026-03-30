#pragma once

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.CompositeAirframe. Do not edit manually. */

typedef enum Aircraft_CompositeAirframe_ValueReference {
  AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M = 0,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M = 1,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M = 2,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG = 3,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG = 4,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT = 5,
} Aircraft_CompositeAirframe_ValueReference;

#ifdef __cplusplus

struct Aircraft_CompositeAirframe_Instance {
  double length_m = 15.0;
  double fuselage_width_m = 3.0;
  double wingspan_m = 10.0;
  int empty_weight_kg = 8573;
  int payload_capacity_kg = 7700;
  int hardpoint_count = 9;
};

inline constexpr Aircraft_FieldBinding Aircraft_CompositeAirframe_Bindings[] = {
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, length_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, fuselage_width_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M, AIRCRAFT_SCALAR_REAL, offsetof(Aircraft_CompositeAirframe_Instance, wingspan_m), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, empty_weight_kg), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, payload_capacity_kg), true},
  {AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT, AIRCRAFT_SCALAR_INTEGER, offsetof(Aircraft_CompositeAirframe_Instance, hardpoint_count), true},
};
inline constexpr size_t Aircraft_CompositeAirframe_BindingCount = sizeof(Aircraft_CompositeAirframe_Bindings) / sizeof(Aircraft_CompositeAirframe_Bindings[0]);

inline constexpr const Aircraft_StringFieldBinding* Aircraft_CompositeAirframe_StringBindings = nullptr;
inline constexpr size_t Aircraft_CompositeAirframe_StringBindingCount = 0;

#endif  /* __cplusplus */