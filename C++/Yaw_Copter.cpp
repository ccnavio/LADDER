/// -*- tab-width: 4; Mode: C++; c-basic-offset: 4; indent-tabs-mode: nil -*-

// **************** ALL YAW CODE ****************

#include <stdlib.h>
#include <cmath>
#include "Copter.h" //you may or may not need this library
#include <RC_Channel/RC_Channel.h>
// #include <AP_AHRS/AP_AHRS.h>
// #include <AP_HAL/AP_HAL.h>

mode_reason_t reason = MODE_REASON_UNKNOWN;

// put your initialisation code here
// this will be called once at start-up
static float init_alt, init_yaw, init_roll, init_pitch;
static int pwm_2; 

// Lets the user know that the code is starting
#ifdef USERHOOK_INIT
void Copter::userhook_init()
{
    cliSerial->printf("\n****************************\n");
    cliSerial->printf("\nInitializing code\n");
    cliSerial->printf("\n****************************\n");

    set_mode(STABILIZE, reason); // Sets back to stabilize mode

    // init_yaw = ahrs.cos_yaw() - ahrs.sin_yaw();

    // // float init_yaw = channel_yaw->get_control_in();
    // cliSerial->printf("Initial yaw: %f \n", init_yaw);
}
#endif

static float error, accum_error, last_error = 0, der_error, output;
static float Kp = 0.135, Ki = 0.09, Kd = 0.0036;
static int pwm_en;

// **************** 100 HZ CODE HERE ****************
// Control yaw code is in here
#ifdef USERHOOK_FASTLOOP
void Copter::userhook_FastLoop()
{
    pwm_en = g.rc_7.get_radio_in();
    if ((pwm_en < 1500) && motors.armed())
    {
        // cliSerial->printf("No safety and flying \n");
        // c_roll = current roll 
        // init_roll = initial roll

        error = (180/M_PI)* asin(sin((ahrs.roll*100 - init_roll)*(M_PI/180)));
        // cliSerial->printf("%f = %f - %f \n", error, ahrs.roll*100, init_roll);
        if (abs(error) > 25)
        {
            // cliSerial->printf("Error greater than 25 \n");
            set_mode(LAND, reason);
        }
        else if (abs(error) > 2)
        {
            accum_error += error * 0.01;
            der_error = (error - last_error)/0.01;
            output = (error * Kp) + (accum_error * Ki) + (der_error * Kd);
            last_error = error;
            pwm_2 += output;
            g.rc_2.set_radio_in(pwm_2); 

            cliSerial->printf("Output = %d \n", pwm_2);
        }
    }
    else if ((pwm_en > 1500) && motors.armed())
    {
        cliSerial->printf("Safety on but flying \n");
        set_mode(STABILIZE, reason); // Sets back to stabilize mode
    }
    else 
    {
        // cliSerial->printf("Should not be running \n");
        // it's not armed so it will do nothing
    }
}
#endif

#ifdef USERHOOK_50HZLOOP
void Copter::userhook_50Hz()
{
    float alt = barometer.get_altitude();
    if (alt - init_alt > 2)
    {
        cliSerial->printf("Automatic safety: exceeded alt allowed\n");
        pwm_en = 1800;
    }
    else
    {
        // do nothing
    }
}
#endif

// **************** 10 HZ CODE HERE ****************
// arming functions must go here
#ifdef USERHOOK_MEDIUMLOOP
void Copter::userhook_MediumLoop()
{

    if (motors.armed() && pwm_en < 1500)
    {
        // cliSerial->printf("Motors are armed \n");
        // This sets channel 3 to 1550
        g.rc_3.set_radio_in(1550); 
        g.rc_3.set_radio_out(1550);
        cliSerial->printf("Radio 3: %d \n", g.rc_3.get_radio_in());
    }
    else // loop and wait for motors to arm
    {
        // cliSerial->printf("Motors not yet armed \n");
    }
}
#endif

// // 3.3 Hz code
#ifdef USERHOOK_SLOWLOOP
void Copter::userhook_SlowLoop()
{
	// cliSerial->printf("Slow Mode\n");	
}
#endif

// 1 Hz code 
#ifdef USERHOOK_SUPERSLOWLOOP
void Copter::userhook_SuperSlowLoop()
{
    if (!motors.armed())
    {
    init_alt = barometer.get_altitude();
    init_roll = ahrs.roll * 100;
    init_pitch = ahrs.pitch * 100;
    init_yaw = ahrs.yaw * 100;
    cliSerial->printf("Roll: %f \n", init_roll);
    cliSerial->printf("Pitch: %f \n", init_pitch);
    cliSerial->printf("Yaw: %f \n", init_yaw);
    cliSerial->printf("Alt: %f \n", init_alt);
    pwm_2 = g.rc_2.get_radio_in();
    }
    else
    {
        // Do nothing
    }
}
#endif



// ------------------------- TIPS AND TRICKS -------------------------
// g.rc_3.set_radio_in(1200); //Sets channel 3 to 1200

// int pwm_en = g.rc_3.get_radio_in(); //Checks value at channel 3

// if (pwm_en == 1200)
// {
//     cliSerial->printf("Function correct\n");
// }