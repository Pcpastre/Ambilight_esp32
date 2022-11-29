

#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <WiFiAP.h>
#include "FS.h"
#include "SPIFFS.h"

#define FORMAT_SPIFFS_IF_FAILED true

#include <FastLED.h>
#define DATA_PIN 15
#define NUM_LEDS 56
CRGB leds[NUM_LEDS];

int arquivo = 0;                                                //Variavel responsavel pela manutenção dos efeitos
int tempo[3]= {1000, 20, 100};                                   //Matriz de tempo usado nos diferentes modos tempo[0] e tempo[3] se refera ao tempo da função pisca() e tempo[1] a função fade() e modoSom()
int RGBB[3] = {255, 255, 255};                                   //Matriz responsavel por guardar as intensidades das cores
int RGBdisplay[3]= {0,0,0}; 
int PINO_LED[3] = {22 , 21 , 23};                                 //Pinos digitais PWM conctados nos led
int canal[3] = {0,1,2};                                         //Matriz responsavel pela manutenção e monitoramente, flag[0] é responsavel por dizer se o led esta ligado ou não flag[1]
int corSelecionada;
int contador = 0;
String comandos[4] = {" ", " ", " ", " "};
String receiv;
String garbage;
void displayColor(String colors);
void RGBSetUp(String colors);
void RGBSetUp2(String colors);
String reg = " ";
boolean waitB = true;
//const char* ssid = "Speers-41801";
//const char* password = "08816009";
WebServer server(80);
String comando;
int flag = -1;
void handleRoot() {
  server.send(200, "text/plain", "LED");
}

void setup(void) {
  Serial.begin(115200);
   FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed
  
   // Configurando os de controle do led como saida como saida
  pinMode(PINO_LED[0], OUTPUT); // LED vermelho
  pinMode(PINO_LED[1], OUTPUT); // LED verde
  pinMode(PINO_LED[2], OUTPUT); // LED azul
  
  ledcAttachPin(PINO_LED[0], 0);//Atribuimos o pino 2 ao canal 0.
  ledcAttachPin(PINO_LED[1], 1);//Atribuimos o pino 2 ao canal 0.
  ledcAttachPin(PINO_LED[2], 2);//Atribuimos o pino 2 ao canal 0.
  ledcSetup(0, 2000, 10);//Atribuimos ao canal 0 a frequencia de 1000Hz com resolucao de 10bits.
  ledcSetup(1, 2000, 10);//Atribuimos ao canal 0 a frequencia de 1000Hz com resolucao de 10bits.
  ledcSetup(2, 2000, 10);//Atribuimos ao canal 0 a frequencia de 1000Hz com resolucao de 10bits.


   if(!SPIFFS.begin(FORMAT_SPIFFS_IF_FAILED)){
        Serial.println("SPIFFS Mount Failed");
        return;
    }

  readFile(SPIFFS, "/info.txt");
  String ssid = (reg.substring(0, reg.indexOf(';')));
  String password = (reg.substring((reg.indexOf(';')+1), reg.length()));
  Serial.print(ssid);Serial.print(' ');Serial.println(password);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid.c_str(), password.c_str());
  Serial.println("");
  int Cwait = 0;
  // Wait for connection
  while(WiFi.status() != WL_CONNECTED && waitB ) {
    delay(500);
    Serial.print(".");
    Cwait++;
    if(Cwait >= 10){
      waitB = false;
      WiFi.mode(WIFI_AP);
      WiFi.softAP("teste", "12345678");
      IPAddress myIP = WiFi.softAPIP();
      Serial.print("AP IP address: ");
      Serial.println(myIP);
      server.begin();

      Serial.println("Server started");
    }
  }
  
  if(waitB){
    Serial.println("");
    Serial.print("Connected to ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  
    if (MDNS.begin("esp32")) {
      Serial.println("MDNS responder started");
    }
  
    server.on("/", handleRoot);
  
    server.on(F("/colorSend"), []() {
      String r = server.arg("R");
      String g = server.arg("G");
      String b = server.arg("B");
      comando = " R=" + r + " " + "G=" + g + " " + "B=" + b + " ";
      RGBSetUp(comando);
      server.send(200, "text/plain", "R= "+r+" G= "+g+" B= "+b);
    });

     server.on(F("/colorSend2"), []() {
      comandos[0] = server.arg("C1");
      comandos[1] = server.arg("C2");
      comandos[2] = server.arg("C3");
      comandos[3] = server.arg("C4");
      RGBSetUp2();
      server.send(200, "text/plain", "work");
    });
  
    server.on(F("/mode"), []() {
      String m = server.arg("M");
      if(m == "SOM"){
        flag = 0;
        server.send(200, "text/plain", "Som Mode");
      }else if(m == "normal"){
        flag = 1;
        server.send(200, "text/plain", "Nomal Mode");
      }
      server.send(200, "text/plain", "Dont find the mode");
    });
  
    server.begin();
    Serial.println("HTTP server started");
  }else{
     server.on("/", sendPage);
     server.on("/conexao", handleInfo);
  }
}

void loop(void) {
 if(waitB){
    server.handleClient();
    if(flag == 0){
      somMode();
    }else if(flag == 1){
      displayColor();
    }
 }else{
    server.handleClient();
 }
}

int somMode(){
 int colorAnt[] = {0,0,0};
 while(true){
      int value = RGBB[contador];
      for(int k = value; k <256; k++){
        server.handleClient();
        if(flag == 1){
          return 0;
        }
        if(colorAnt[0] != RGBdisplay[0] || colorAnt[1] != RGBdisplay[1] ||colorAnt[2] != RGBdisplay[2]){ 
           ledcWrite(canal[0], (RGBdisplay[0]*4));
           ledcWrite(canal[1], (RGBdisplay[1]*4));
           ledcWrite(canal[2], (RGBdisplay[2]*4));
           delay(150);
        }
        colorAnt[0] = RGBdisplay[0];
        colorAnt[1] = RGBdisplay[1];
        colorAnt[2] = RGBdisplay[2];
        ledcWrite(canal[0], (RGBB[0]*4));
        ledcWrite(canal[1], (RGBB[1]*4));
        ledcWrite(canal[2], (RGBB[2]*4));
        if(contador == 0){
          RGBB[0] = k;
          RGBB[2] = (255) - k;
          RGBB[1] = 0;
        }else if(contador == 1){
          RGBB[1] = k;
          RGBB[0] = (255) - k;
          RGBB[2] = 0;
        }else if(contador == 2){
          RGBB[2] = k;
          RGBB[1] = (255) - k;
          RGBB[0] = 0;
        }
        delay(10);
       }
    contador++;
   if(contador > 2){
      contador = 0;
   }
 }
}

void RGBSetUp(String colors){
  for(int i = 0; i<3; i++){
    RGBdisplay[i] = 0;
  }
  char colorChar[colors.length()];
  for (int i=0;i<colors.length();i++){

    //Armazena na string (array de char)

    colorChar[i] = colors.charAt(i);
    Serial.println(colorChar[i] );
  }
  // flag[1] = 1;
  int pos = 0;
  int posA = 0;
  for(int i = 0; i < 3; i++){
    pos = colors.indexOf(" ", posA+1);
      for(int j = 0; j < (pos-(posA+3)); j++){
        RGBdisplay[i] = ((colorChar[pos-1-j]-'0'))*pow(10,j)+RGBdisplay[i];
      }
    posA = pos;
  }
}

void RGBSetUp2(){
  for(int i = 0; i < 4; i++){
    String dataRec = comandos[i];
    int red = x2i(dataRec.substring(0, 2));
    int green = x2i(dataRec.substring(2, 4));
    int blue = x2i(dataRec.substring(4, 6));

    if(i == 0){
      for(int j = 0; j<4; j++){
        leds[j] = CRGB(red,green,blue);
      }
    }else if(i == 1){
      for(int j = 10; j<20; j++){
        leds[j] = CRGB(red,green,blue);
      }
    }else if(i == 2){
      for(int j = 33; j<41; j++){
        leds[j] = CRGB(red,green,blue);
      }
    }else if(i == 3){
      for(int j = 47; j<51; j++){
        leds[j] = CRGB(red,green,blue);
      }
    }
    dataRec = " ";
  }
   FastLED.show();
}

int x2i(String s) 
{
  int x = 0;
  int n = s.length();
  char c[n + 1];
  strcpy(c, s.c_str());
  for(int i = 0;i < (n+1);i++) {
    
    if (c[i] >= '0' && c[i] <= '9') {
      x *= 16;
      x += c[i] - '0'; 
    }
    else if (c[i] >= 'a' && c[i] <= 'f') {
      x *= 16;
      x += (c[i] - 'a') + 10; 
    }
    else break;
  }
  return x;
}

void displayColor(){

  for(int j = 0; j <3; j++){
    if(RGBB[j] >= RGBdisplay[j]){
      for(int i = RGBdisplay[j]; i < RGBB[j]; i = i +4){
          ledcWrite(canal[j], i*4 ); // Liga LED  vermelho
         RGBB[j] = RGBdisplay[j];
         delay(50);
      }
    }else{
      for(int i = RGBdisplay[j]; i > RGBB[j]; i = i -4){
          ledcWrite(canal[j], i*4 ); // Liga LED vermelho
         RGBB[j] = RGBdisplay[j];
         delay(50);
      }
    }
   }
}

void sendPage(){
 

  String page = htmlPage(0,0);
  server.send(200, "text/html", page);
  

}

String htmlPage(float t, float p){
   String cd = "<!DOCTYPE html>\n";
   cd += "<html lang=\"pt-br\">\n";
  cd += "<head>\n";
  cd += "<meta charset=\"UTF-8\">\n";
  cd += "<meta http-equiv=\"X-UA-Compatible\" content=\"IE=edge\">\n";
  cd += "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  cd += "<title>Rede Wifi</title>\n";
  cd += "<style>\n";
  cd += "html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  cd += "body{margin-top: 50px;} \n";
  cd += "h1 {color: #444444; margin: 50px auto 30px;}\n";
  cd += "p {font-size: 24px; color: #444444; margin-bottom: 10px;}\n";
  cd += "</style>\n";
  cd += "</head>\n";
  cd += "<body>\n";
  cd += "<div id=\"webpage\">\n";
  cd += "<form action=\"/conexao\" method=\"GET\">\n";
  cd += "SSID:\n";
  cd += "<input name=\"ssid\" type=\"text\" value=\"Seu SSID\" />\n";
  cd += "SENHA:\n";
  cd += "<input name=\"senha\" type=\"text\" value=\"Sua Senha\" />\n";;
  cd += "<input type=\"submit\" value=\"Enviar\" /></form>\n";
  cd += "</div>\n";
  cd += "</body>\n";  
  cd += "</html>\n";
  return cd;             


}

void handleInfo(){
  String ssid = server.arg("ssid");
  String senha = server.arg("senha");
  String value = ssid+';'+senha+"\n";
  writeFile(SPIFFS, "/info.txt", (value.c_str()));
  server.send(200, "text/plain", "ssid: " + ssid+ " senha: "+senha+ "\n" + "Restarting");
  ESP.restart();

}

void writeFile(fs::FS &fs, const char * path, const char * message){
    Serial.printf("Writing file: %s\r\n", path);

    File file = fs.open(path, FILE_WRITE);
    if(!file){
        Serial.println("- failed to open file for writing");
        return;
    }
    if(file.print(message)){
        Serial.println("- file written");
    } else {
        Serial.println("- write failed");
    }
    file.close();
}

void deleteFile(fs::FS &fs, const char * path){
    Serial.printf("Deleting file: %s\r\n", path);
    if(fs.remove(path)){
        Serial.println("- file deleted");
    } else {
        Serial.println("- delete failed");
    }
}

void readFile(fs::FS &fs, const char * path){
    Serial.printf("Reading file: %s\r\n", path);

    File file = fs.open(path);
    if(!file || file.isDirectory()){
        Serial.println("- failed to open file for reading");
        return;
    }
    
    Serial.println("- read from file:");
    while(file.available()){
        reg = file.readStringUntil('\n');
        //Serial.write(file.read());
    }
    file.close();
}
