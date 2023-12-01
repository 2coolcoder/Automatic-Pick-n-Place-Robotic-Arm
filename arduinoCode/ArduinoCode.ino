int q0,q1,q2, contact_sw=0;
bool magnet=0;

#define dir1 6
#define step1 7
#define dir2 8
#define step2 9
#define dir3 10
#define step3 11
#define switch1 2
#define switch2 3
#define magnetPin 12
void move(int step_pin, int dir_pin, int steps)
{
    digitalWrite(dir_pin, steps>0 ? HIGH : LOW);
    if(steps<0)
      steps=-steps;
    for (int i = 0; i < steps; i++)
    { 
        digitalWrite(step_pin, HIGH);
        digitalWrite(step_pin, LOW);
        delay(30);
    }
}

class motor
{
    public:
    int pos1, pos2, pos3;
    motor()
    {
        pos1 = 0;
        pos2 = 0;
        pos3 = 0;
    }
    void move1(int newPos)
    {
        newPos*=2.5;
        int delta = newPos - pos1;
//        if (delta>450)
//        delta=delta-900;
//        else if(delta<-450)
//        delta= delta+900;

        move(step1, dir1, -delta);
        pos1 = newPos;
    }
    void move2(int newPos)
    {
        newPos*=3.3333;
        int delta = newPos - pos2;
//        if (delta>600)
//        delta=delta-1200;
//        else if(delta<-600)
//        delta= delta+1200;

        move(step2, dir2, delta);
        pos2 = newPos;
    }
    void move3(int newPos)
    {
        newPos*=3.3333;
        int delta = newPos - pos3;
//        if (delta>600)
//        delta=delta-1200;
//        else if(delta<-600)
//        delta= delta+1200;

        move(step3, dir3, -delta);
        pos3 = newPos;
    }
};
motor M;
void setup()
{
    Serial.begin(115200); 
    //Serial.setTimeout(1); 
    int opPins[] =  {step1, step2, step3, dir1, dir2, dir3} ;
    for (int i = 0; i < 6;i++)
        pinMode(opPins[i], OUTPUT);
    pinMode(switch1, INPUT_PULLUP);
    pinMode(switch2, INPUT_PULLUP);    
    pinMode(13,OUTPUT);
    pinMode(magnetPin,OUTPUT);
    digitalWrite(13,HIGH);
    
//    while(1)
//    {
//      //delay(1000);
//     M.move1(20);
//    delay(1000);
//    M.move2(20);
//    delay(1000);
//    M.move3(-20);
//    delay(1000);
//    
//   
//    
//    }
//    
//    M.move3(190);
//    delay(500);
//    M.move3(10);
}
void loop()
{
  //contact_sw= (digitalRead(switch1)?1:0) + (digitalRead(switch2)?1:0);
  contact_sw = 2 - digitalRead(switch1) - digitalRead(switch2);
  while(!Serial.available() || Serial.read()!='s');
  while(Serial.available()<16);
  magnet= Serial.read()-'0';
  if(magnet)
      digitalWrite(magnetPin,HIGH);
     else
     digitalWrite(magnetPin,LOW);
  Serial.print(magnet);
  q0=Serial.parseInt();
  q1=Serial.parseInt();
  q2=Serial.parseInt();
  if(Serial.available() && Serial.read()=='e')
  {
//    Serial.print(q0);
//    Serial.print(q1);
//    Serial.print(q2);
    Serial.print(contact_sw);
    Serial.println("Success");
    M.move1(q0);
    delay(500);
    M.move2(q1);
    delay(500);
    M.move3(q2);
    delay(500);
  }
  else
  {
//    Serial.print(q0);
//    Serial.print(" ");
//    Serial.print(q1);
//    Serial.print(" ");
//    Serial.print(q2);
//    Serial.print(" ");
      Serial.print(contact_sw);
      Serial.println("Fail");
  }
  Serial.flush();
//  Serial.println(q0);
//  Serial.println(q1);
//  Serial.println(q2);
  
}
