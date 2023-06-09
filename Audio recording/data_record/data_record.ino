/*
  This example reads audio data from the on-board PDM microphones, and prints
  out the samples to the Serial console. The Serial Plotter built into the
  Arduino IDE can be used to plot the audio data (Tools -> Serial Plotter)

  Circuit:
  - Arduino Nano 33 BLE board, or
  - Arduino Nano RP2040 Connect, or
  - Arduino Portenta H7 board plus Portenta Vision Shield

  This example code is in the public domain.
*/

#include <PDM.h>
// Flag to indicate if noise has been detected
bool noiseDetected = false;



int noiseThreshold = 200;
int timeSet = 2.5;
int samplesSet = 1600 * timeSet;
int samplesRecorded = 0;


// Time when noise was detected
unsigned long noiseDetectedTime;

// default number of output channels
static const char channels = 1;

// default PCM output frequency
static const int frequency = 16000;

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512];

// Number of audio samples read
volatile int samplesRead;

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);

  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and 24 on the Portenta Vision Shield
  // PDM.setGain(30);

  // Initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate for the Arduino Nano 33 BLE Sense
  // - a 32 kHz or 64 kHz sample rate for the Arduino Portenta Vision Shield
  if (!PDM.begin(channels, frequency)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }
}
void loop() {
  // Wait for samples to be read
  if (samplesRead) {
    // Check if noise has been detected
    if (!noiseDetected) {
      // Check if there is noise above the threshold
      for (int i = 0; i < samplesRead; i++) {
        if (sampleBuffer[i] > noiseThreshold || sampleBuffer[i] < -noiseThreshold) {
          noiseDetected = true;
          samplesRecorded = 0;
          break;
        }
      }
    } else {
      // Noise has been detected, print data for 10 seconds
      if (samplesRecorded < samplesSet) {
        unsigned long tiempoInicio = millis();
        for (int i = 0; i < samplesRead; i++) {
          //Serial.println(sampleBuffer[i]);
          unsigned long tiempoFinal = millis();
          unsigned long duracionCiclo = tiempoFinal - tiempoInicio;
          //Serial.println(duracionCiclo);
          Serial.println(samplesRecorded);
          samplesRecorded ++;
        }
      } else {
        // Reset variables after 10 seconds
        noiseDetected = false;
        
      }
    }

    // Clear the read count
    samplesRead = 0;
  }
}

/**
 * Callback function to process the data from the PDM microphone.
 * NOTE: This callback is executed as part of an ISR.
 * Therefore using `Serial` to print messages inside this function isn't supported.
 * */
void onPDMdata() {
  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable/2;
}