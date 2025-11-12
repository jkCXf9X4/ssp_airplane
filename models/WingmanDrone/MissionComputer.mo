within WingmanDrone;
model MissionComputer
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real redundancyLevel = 3;
  parameter Real computeBudgetTOPS = 25;
  Interfaces.RealInput manualInput;
  Interfaces.RealInput autonomyPort;
  Interfaces.RealInput powerIn;
  Interfaces.RealInput fuelStatus;
  Interfaces.RealOutput engineThrottle;
  Interfaces.RealOutput surfaceBus;
  Interfaces.RealOutput flightStatus;
  Interfaces.RealOutput orientationEuler;
  Interfaces.RealOutput locationLLA;
protected
  Real blendCmd;
  Real powerFactor;
  Real headingDeg(start=0);
  Real positionKm(start=0);
  parameter Real headingGain = 60;
  parameter Real velocityGain = 180;
equation
  blendCmd = 0.6 * autonomyPort + 0.4 * manualInput;
  powerFactor = min(1.0, max(0.2, powerIn)) * max(0.0, min(1.0, fuelStatus));
  engineThrottle = min(1.0, max(0.1, blendCmd * powerFactor));
  surfaceBus = min(1.0, engineThrottle + 0.1 * powerFactor);
  flightStatus = 0.35 * engineThrottle + 0.35 * surfaceBus + 0.15 * (orientationEuler / 360) + 0.15 * fuelStatus;
  der(headingDeg) = headingGain * (manualInput - 0.5) + 20 * (autonomyPort - 0.5);
  der(positionKm) = velocityGain * engineThrottle;
  orientationEuler = headingDeg;
  locationLLA = positionKm;
end MissionComputer;
