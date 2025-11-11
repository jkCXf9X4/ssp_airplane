within SSPAirplane;
model WingSystem
  import Modelica.SIunits;
  parameter SI.Area referenceArea = 134;
  parameter SI.Length span = 35.8;
  parameter Real wingAreaScale(min=0.6, max=1.4) = 1.0;
  parameter Real aspectRatio = 9.6;
  Modelica.Blocks.Interfaces.RealInput liftCommand "0..1 command from control";
  Modelica.Blocks.Interfaces.RealOutput liftCoefficient;
  Modelica.Blocks.Interfaces.RealOutput effectiveArea "Scaled wing area";
protected
  parameter Real baseLiftCoeff = 0.45;
equation
  effectiveArea = referenceArea * wingAreaScale;
  liftCoefficient = baseLiftCoeff * wingAreaScale * liftCommand;
end WingSystem;
