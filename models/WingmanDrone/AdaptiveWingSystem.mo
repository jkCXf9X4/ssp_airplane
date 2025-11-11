within WingmanDrone;
model AdaptiveWingSystem
  import Interfaces = WingmanDrone.Interfaces;
  parameter Real referenceArea = 28 "m2";
  parameter Real span = 7.3 "m";
  parameter Real wingAreaScale(min=0.7, max=1.3) = 1.0;
  parameter Real aspectRatio = 5.5;
  Interfaces.RealInput controlSurfaces "0..1 command from mission computer";
  Interfaces.RealOutput liftInterface;
  Interfaces.RealOutput effectiveArea "Scaled wing area";
protected
  parameter Real baseLiftCoeff = 0.6;
equation
  effectiveArea = referenceArea * wingAreaScale;
  liftInterface = baseLiftCoeff * wingAreaScale * controlSurfaces;
end AdaptiveWingSystem;
