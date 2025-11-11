within SSPAirplane;
model WingSystem
  import Interfaces = SSPAirplane.Interfaces;
  parameter Real referenceArea = 134 "m2";
  parameter Real span = 35.8 "m";
  parameter Real wingAreaScale(min=0.6, max=1.4) = 1.0;
  parameter Real aspectRatio = 9.6;
  Interfaces.RealInput liftCommand "0..1 command from control";
  Interfaces.RealOutput liftCoefficient;
  Interfaces.RealOutput effectiveArea "Scaled wing area";
protected
  parameter Real baseLiftCoeff = 0.45;
equation
  effectiveArea = referenceArea * wingAreaScale;
  liftCoefficient = baseLiftCoeff * wingAreaScale * liftCommand;
end WingSystem;
