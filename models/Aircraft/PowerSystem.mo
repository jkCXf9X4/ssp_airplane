within Aircraft;
model PowerSystem
  import GI = Aircraft.GeneratedInterfaces;
  parameter Real busVoltageKV = 0.27;
  parameter Real bufferCapacityMJ = 650;
  parameter Real distributionEfficiency = 0.97;
  input GI.GenericElectricalBus generatorInput;
  output GI.GenericElectricalBus avionicsFeed;
  output GI.GenericElectricalBus controlFeed;
  output GI.GenericElectricalBus autonomyFeed;
protected
  parameter Real controlShare = 0.25;
  parameter Real autonomyShare = 0.2;
  Real availableKW;
equation
  availableKW = generatorInput.available_power_kw * distributionEfficiency + bufferCapacityMJ * 0.277777;
  controlFeed.available_power_kw = availableKW * controlShare;
  autonomyFeed.available_power_kw = availableKW * autonomyShare;
  avionicsFeed.available_power_kw = max(0, availableKW - controlFeed.available_power_kw - autonomyFeed.available_power_kw);

  controlFeed.voltage_kv = busVoltageKV;
  autonomyFeed.voltage_kv = busVoltageKV;
  avionicsFeed.voltage_kv = busVoltageKV;

  controlFeed.current_a = controlFeed.available_power_kw * 1000 / (busVoltageKV * 1000);
  autonomyFeed.current_a = autonomyFeed.available_power_kw * 1000 / (busVoltageKV * 1000);
  avionicsFeed.current_a = avionicsFeed.available_power_kw * 1000 / (busVoltageKV * 1000);
end PowerSystem;
