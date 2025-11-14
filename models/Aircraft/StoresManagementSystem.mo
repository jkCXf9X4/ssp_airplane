within Aircraft;
model StoresManagementSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Integer totalStationCount = 9;
  parameter Real coolingCapacityKW = 12;
  parameter Integer defaultMask = 511;
  input GI.StoresCommandBus storesBusIn;
  input GI.GenericElectricalBus powerIn;
  input GI.StructuralInterface airframeMount;
  input GI.StructuralPerformanceState performanceStatus;
  output GI.StoresStatusBus storesTelemetry;
protected
  Real powerAdequacy;
  Real coolingUsage;
  Integer stationMask;
equation
  stationMask = if storesBusIn.power_mode_mask > 0 then storesBusIn.power_mode_mask else defaultMask;
  powerAdequacy = min(1.0, max(0.0, powerIn.available_power_kw / max(1.0, totalStationCount * 2.0)));
  coolingUsage = min(coolingCapacityKW, powerAdequacy * coolingCapacityKW + abs(airframeMount.bending_moment_knm) * 0.05);

  storesTelemetry.store_present_mask = stationMask;
  storesTelemetry.weapon_ready_mask = if performanceStatus.stores_release_inhibit then 0 else stationMask;
  storesTelemetry.store_mass_total_kg = totalStationCount * 250 * powerAdequacy;
  storesTelemetry.cooling_demand_kw = coolingUsage;
  storesTelemetry.fault_code = if powerAdequacy < 0.2 then 101 else if performanceStatus.stores_release_inhibit then 55 else 0;
end StoresManagementSystem;
