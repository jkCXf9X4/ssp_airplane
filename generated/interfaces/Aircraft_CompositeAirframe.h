#ifndef AIRCRAFT_COMPOSITEAIRFRAME_H
#define AIRCRAFT_COMPOSITEAIRFRAME_H

#include "Aircraft_InterfaceCommon.h"

/* Generated interface for Aircraft.CompositeAirframe. Do not edit manually. */

typedef enum Aircraft_CompositeAirframe_ValueReference {
  AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M = 0,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M = 1,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M = 2,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG = 3,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG = 4,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT = 5,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH = 6,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGEWIDTH = 7,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN = 8,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOADSCALE = 9,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_MAXPAYLOAD = 10,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTYMASS = 11,
  AIRCRAFT_COMPOSITEAIRFRAME_VR_WETTEDAREAFACTOR = 12,
} Aircraft_CompositeAirframe_ValueReference;

enum { Aircraft_CompositeAirframe_VrCount = 13 };

#ifdef __cplusplus
#include <string>

struct Aircraft_CompositeAirframe_Instance {
  Aircraft_VrMapping vr_map[13] = {};
  double length_m = 15;
  double fuselage_width_m = 3;
  double wingspan_m = 10;
  double empty_weight_kg = 8573;
  double payload_capacity_kg = 7700;
  int hardpoint_count = 9;
  double length = 15;
  double fuselageWidth = 3;
  double wingspan = 10;
  double payloadScale = 1;
  double maxPayload = 7700;
  double emptyMass = 8573;
  double wettedAreaFactor = 2.2;
};

inline void Aircraft_CompositeAirframe_initialize_vr_map(Aircraft_CompositeAirframe_Instance* instance) {
  for (size_t i = 0; i < Aircraft_CompositeAirframe_VrCount; ++i) {
    instance->vr_map[i] = {nullptr, AIRCRAFT_DATA_NONE, false};
  }
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH_M] = {&instance->length_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGE_WIDTH_M] = {&instance->fuselage_width_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN_M] = {&instance->wingspan_m, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTY_WEIGHT_KG] = {&instance->empty_weight_kg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOAD_CAPACITY_KG] = {&instance->payload_capacity_kg, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_HARDPOINT_COUNT] = {&instance->hardpoint_count, AIRCRAFT_DATA_INTEGER, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_LENGTH] = {&instance->length, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_FUSELAGEWIDTH] = {&instance->fuselageWidth, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_WINGSPAN] = {&instance->wingspan, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_PAYLOADSCALE] = {&instance->payloadScale, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_MAXPAYLOAD] = {&instance->maxPayload, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_EMPTYMASS] = {&instance->emptyMass, AIRCRAFT_DATA_REAL, true};
  instance->vr_map[AIRCRAFT_COMPOSITEAIRFRAME_VR_WETTEDAREAFACTOR] = {&instance->wettedAreaFactor, AIRCRAFT_DATA_REAL, true};
}

#endif  /* __cplusplus */
#endif  /* AIRCRAFT_COMPOSITEAIRFRAME_H */