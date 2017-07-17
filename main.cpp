#include <iostream>

using namespace std;

int main()
{
    double pe = 0;
    double integral = 0;
    double error, setpoint = 0, mv = 10, dt = 0.1, output, derivative;
    double Kp = 1, Ki = 1, Kd = 0.01;

    for( int i = 0; i < 50; i++ ){
        error = setpoint - mv;
        cout << "Error: " << error << endl;
        integral += error*dt;
        derivative = (error - pe)/dt;
        output = Kp*error + Ki*integral + Kd*derivative;
        cout << "Output: " << output << endl << endl;
        pe = error;
        mv += error;
    }

    return 0;
}
