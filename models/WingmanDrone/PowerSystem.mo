within WingmanDrone;
model PowerSystem
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real busVoltageKV = 1.2;
  parameter Real bufferCapacityMJ = 500;
  parameter Real distributionEfficiency = 0.95;
  Interfaces.RealInput generatorInput;
  Interfaces.RealOutput avionicsFeed;
  Interfaces.RealOutput controlFeed;
  Interfaces.RealOutput autonomyFeed;
protected
  parameter Real controlShare = 0.2;
  parameter Real autonomyShare = 0.25;
  Real availableMW;
equation
  availableMW = generatorInput * distributionEfficiency + bufferCapacityMJ / 3600;
  controlFeed = availableMW * controlShare;
  autonomyFeed = availableMW * autonomyShare;
  avionicsFeed = max(0, availableMW - controlFeed - autonomyFeed);
end PowerSystem;
