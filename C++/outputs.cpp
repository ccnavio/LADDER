#include <stdlib.h>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

int main()
{	
	const int size = 50;
	char testline[size];
	char crap[size];
	char crap2[size];
	fstream myfile;
	myfile.open ("plah.txt", ios::in | ios::out);
	while (!myfile.eof())
	{
		myfile.getline(testline, size);
		myfile.getline(crap, size);
		myfile.getline(crap2, size);
		cout<<testline<<endl;
	}
	myfile.close();
	cout<<"Done\n";
	return 0;
}