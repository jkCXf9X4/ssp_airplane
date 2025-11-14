within Aircraft;
model PowerSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real busVoltageKV = 0.27;
  parameter Real acBusVoltageKV = 0.115;
  parameter Real bufferCapacityMJ = 650;
  parameter Real distributionEfficiency = 0.97;
  input GI.GenericElectricalBus generatorInput;
  input GI.GenericElectricalBus emergencyInput;
  output GI.GenericElectricalBus avionicsFeed;
  output GI.GenericElectricalBus controlFeed;
  output GI.GenericElectricalBus autonomyFeed;
  output GI.GenericElectricalBus storesFeed;
  output GI.GenericElectricalBus dcBus270;
  output GI.GenericElectricalBus acBus115;
  output GI.GenericElectricalBus emergencyBus;
protected
  parameter Real controlShare = 0.25;
  parameter Real autonomyShare = 0.2;
  parameter Real storesShare = 0.18;
  Real bufferKW;
  Real generatorKW;
  Real totalKW;
  Real controlKW;
  Real autonomyKW;
  Real storesKW;
  Real avionicsKW;
  Real dcKW;
  Real acKW;
  Real emergencyKW;
equation
  bufferKW = bufferCapacityMJ * 0.277777;
  generatorKW = (generatorInput.available_power_kw + max(0, generatorInput.voltage_kv * generatorInput.current_a)) * distributionEfficiency;
  totalKW = max(0, generatorKW + bufferKW);
  controlKW = totalKW * controlShare;
  autonomyKW = totalKW * autonomyShare;
  storesKW = totalKW * storesShare;
  avionicsKW = max(0, totalKW - controlKW - autonomyKW - storesKW);
  dcKW = avionicsKW * 0.65;
  acKW = avionicsKW - dcKW;
  emergencyKW = emergencyInput.available_power_kw;

  controlFeed.available_power_kw = controlKW;
  autonomyFeed.available_power_kw = autonomyKW;
  storesFeed.available_power_kw = storesKW;
  avionicsFeed.available_power_kw = avionicsKW;
  dcBus270.available_power_kw = dcKW;
  acBus115.available_power_kw = acKW;
  emergencyBus.available_power_kw = emergencyKW + 0.1 * totalKW;

  controlFeed.voltage_kv = busVoltageKV;
  autonomyFeed.voltage_kv = busVoltageKV;
  storesFeed.voltage_kv = busVoltageKV;
  avionicsFeed.voltage_kv = busVoltageKV;
  dcBus270.voltage_kv = busVoltageKV;
  acBus115.voltage_kv = acBusVoltageKV;
  emergencyBus.voltage_kv = busVoltageKV;

  controlFeed.current_a = if controlFeed.voltage_kv > 1e-6 then controlKW * 1000 / (controlFeed.voltage_kv * 1000) else 0;
  autonomyFeed.current_a = if autonomyFeed.voltage_kv > 1e-6 then autonomyKW * 1000 / (autonomyFeed.voltage_kv * 1000) else 0;
  storesFeed.current_a = if storesFeed.voltage_kv > 1e-6 then storesKW * 1000 / (storesFeed.voltage_kv * 1000) else 0;
  avionicsFeed.current_a = if avionicsFeed.voltage_kv > 1e-6 then avionicsKW * 1000 / (avionicsFeed.voltage_kv * 1000) else 0;
  dcBus270.current_a = if dcBus270.voltage_kv > 1e-6 then dcKW * 1000 / (dcBus270.voltage_kv * 1000) else 0;
  acBus115.current_a = if acBus115.voltage_kv > 1e-6 then acKW * 1000 / (acBus115.voltage_kv * 1000) else 0;
  emergencyBus.current_a = if emergencyBus.voltage_kv > 1e-6 then emergencyBus.available_power_kw * 1000 / (emergencyBus.voltage_kv * 1000) else 0;
end PowerSystem;
