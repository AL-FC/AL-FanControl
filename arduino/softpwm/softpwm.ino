#include <SoftPWM.h>

void setup()
{
  SoftPWMBegin();
  
  SoftPWMSet(8, 0);

  SoftPWMSetFadeTime(8, 1000, 1000);
}

void loop()
{
  SoftPWMSet(8, 255);
  delay(2000);
  SoftPWMSet(8, 0);
  delay(2000);
}
