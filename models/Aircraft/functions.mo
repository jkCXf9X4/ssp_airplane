within Aircraft;
function stringToRealVector
  "Split a string into substrings and parse them as Reals"
  import Modelica.Utilities.Strings;

  input String str                  "e.g. \"1.0, 2.5, -3.7\"";
  input String delimiter = ","      "Single-character delimiter";
  output Real values[:]             "Parsed Real values";
protected
  Integer nDelims;
  Integer n;
  Integer startIndex;
  Integer delimIndex;
  Integer i;
  String token;
algorithm
  // How many numbers? (#delimiters + 1)
  nDelims := Strings.count(str, delimiter);
  n := nDelims + 1;
  values := fill(0.0, n);

  startIndex := 1;
  for i in 1:n loop
    // Find next delimiter (0 means: not found)
    delimIndex := Strings.find(str, delimiter, startIndex);

    if delimIndex == 0 then
      // Last token goes to end of string
      token := Strings.substring(
                 str,
                 startIndex,
                 Strings.length(str));
    else
      token := Strings.substring(
                 str,
                 startIndex,
                 delimIndex - 1);
    end if;

    // scanReal ignores leading whitespace, so "  1.23" is fine
    values[i] := Strings.scanReal(token);

    // Next token starts after the delimiter
    startIndex := delimIndex + 1;
  end for;
end stringToRealVector;

// Usage
// model TestStringToRealVector
//   Real x[:];
// equation
//   x = YourPackage.stringToRealVector("1.0, 2.5, -3.7");
//   // x = {1.0, 2.5, -3.7}
// end TestStringToRealVector;