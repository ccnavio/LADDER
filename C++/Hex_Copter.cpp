/// -*- tab-width: 4; Mode: C++; c-basic-offset: 4; indent-tabs-mode: nil -*-

// **************** ALL CENTER CODE ****************

#include <stdlib.h>
#include <cmath>
#include "Copter.h" //you may or may not need this library
#include <RC_Channel/RC_Channel.h>
// #include <AP_AHRS/AP_AHRS.h>

mode_reason_t reason = MODE_REASON_UNKNOWN;

// put your initialisation code here
// this will be called once at start-up
static float init_alt, init_yaw, init_roll, init_pitch;
// static int pwm_2;
static int count; 

// // Lets the user know that the code is starting
#ifdef USERHOOK_INIT
void Copter::userhook_init()
{
    // cliSerial->printf("\n****************************\n");
    // cliSerial->printf("\n     Initializing code\n");
    // cliSerial->printf("\n****************************\n");
    // count = 0;
    // // set_mode(STABILIZE, reason); // Sets back to stabilize mode
    // // hal.rcout->enable_ch(3);
    // // init_yaw = ahrs.cos_yaw() - ahrs.sin_yaw();

    // // // float init_yaw = channel_yaw->get_control_in();
    // // cliSerial->printf("Initial yaw: %f \n", init_yaw);
}
#endif

// // static float error, accum_error, last_error = 0, der_error, output;
// // static float Kp = 0.135, Ki = 0.09, Kd = 0.0036;
// static int pwm_en;

// // **************** 100 HZ CODE HERE ****************
// // Control yaw code is in here
#ifdef USERHOOK_FASTLOOP
void Copter::userhook_FastLoop()
{
    // pwm_en = g.rc_7.get_radio_in();
    // if ((pwm_en < 1500) && motors.armed())
    // {
    //     // auto_takeoff_set_start_alt();    
    //     // cliSerial->printf("hovering at %f \n", barometer.get_altitude());
    // }
    // else if ((pwm_en > 1500) && motors.armed())
    // {
    //     // Flying manually
    // }
    // else 
    // {
    //     // When disarmed
    // }
}
#endif

#ifdef USERHOOK_50HZLOOP
void Copter::userhook_50Hz()
{
    // float alt = barometer.get_altitude();
    // if ((alt - init_alt) > 2)
    // {
    //     cliSerial->printf("Automatic safety: exceeded alt allowed\n");
    //     pwm_en = 1800;
    // }
    // else
    // {
    //     // do nothing
    // }
}
#endif

// **************** 10 HZ CODE HERE ****************
// arming functions must go here
#ifdef USERHOOK_MEDIUMLOOP
void Copter::userhook_MediumLoop()
{
    int pwm_en = g.rc_7.get_radio_in();
    if (motors.armed() && (g.rc_3.get_radio_in() > g.rc_3.get_radio_min()) && (barometer.get_altitude() - init_alt) < 1)
    {
        count += 1;
        if (count == 100)
        {
            !motors.armed();
        }
    }
    else // loop and wait for motors to arm
    {
        // cliSerial->printf("Motors not yet armed \n");
    }
}
#endif

// // // 3.3 Hz code
#ifdef USERHOOK_SLOWLOOP
void Copter::userhook_SlowLoop()
{

}
#endif

static int first;
// 1 Hz code 
#ifdef USERHOOK_SUPERSLOWLOOP
void Copter::userhook_SuperSlowLoop()
{
    init_alt = barometer.get_altitude();
    init_roll = ahrs.roll * 100;
    init_pitch = ahrs.pitch * 100;
    init_yaw = ahrs.yaw * 100;
    cliSerial->printf("\nRoll: %f \n", init_roll);
    cliSerial->printf("Pitch: %f \n", init_pitch);
    cliSerial->printf("Yaw: %f \n", init_yaw);
    cliSerial->printf("Alt: %f \n", init_alt);
    // pwm_2 = g.rc_2.get_radio_in();
    // else if (motors.armed() && first != 1)
    // {
    //     first = 1;
    //     // g.rc_3.set_radio_out(1500);
    //     g.rc_3.set_radio_in(1500);
    //     cliSerial->printf("Throttle in: %f \n", g.rc_3.get_radio_in());
    //     // cliSerial->printf("Throttle out: %f \n", g.rc_3.get_radio_out());    
    //     cliSerial->printf("Taking off hopefully\n");
    //     // Do nothing
    // }
    //     cliSerial->printf("Hovering at %f \n", barometer.get_altitude());

}
#endif

// ------------------------- TIPS AND TRICKS -------------------------
// g.rc_3.set_radio_in(1200); //Sets channel 3 to 1200

// int pwm_en = g.rc_3.get_radio_in(); //Checks value at channel 3

// if (pwm_en == 1200)
// {
//     cliSerial->printf("Function correct\n");
// }