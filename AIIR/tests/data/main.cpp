#include <fstream>
#include <iostream>
#include <cmath>
#include <math.h>
#include <ctime>
#include <limits>


int cityamount;
int **distances;


bool fileread(char*);
bool result(int, char**);
void filewrite(int*, int, char**, double);
void writetab(int**);
void TabuSearch(int, char**);

int  main(int argc,char  *argv[])
{
    if(argc < 5)
        { std::cout << "\nPodano zle arg wejsciowe"; return 0; }
    srand(time(NULL));
    if(fileread(argv[3]) == 0)
        std::cout << "\n OTWIERANIE PLIKU Z MACIERZA NIE POWIODLO SIE DLA PODANYCH DANYCH WEJSCIOWYCH!!!";
    else
        TabuSearch(argc, argv);
}



bool fileread(char *filen)         // funkcja do odczytywania danych z pliku
{
    std::string filename = filen;
    std::fstream plik;
    plik.open(filename,std::ios::in);
    if(plik.good())                         // sprawdzenie poprawnosci wczytania pliku, w razie niepowodzenia zwracamy blad
    {
        plik>>cityamount;
        distances = new int* [cityamount];   // dwuwymiarowa tablica dynamiczna
        for(int i=0;i<cityamount;++i)
            distances[i]=new int[cityamount];
        for(int i=0;i<cityamount;++i)       // zapelnianie tablicy danymi z pliku
            for(int j=0;j<cityamount;++j)
                plik>>distances[i][j];
        plik.close();
        return 1;
    }
    plik.close();
    return 0;
}

bool result(int cost, char  *argv[])         // funkcja do zapisywania danych do pliku
{
    int oldCost;
    std::string oldName, currentName = argv[3];
    std::string filename = argv[4];
    std::fstream plik;
    plik.open(filename,std::ios::in);
    if(plik.good())                         // sprawdzenie poprawnosci wczytania pliku, w razie niepowodzenia zwracamy blad
    {
        plik>>oldName;
        plik>>oldCost;
        plik.close();
        if(oldCost > cost || oldName.compare(currentName)){
            std::cout << "\nsprawdzam";
            return 1;
        }
        return 0;
    }
    plik.close();
    return 1;
}

void filewrite(int* sequence, int cost, char  *argv[], double czas)
{
    std::ofstream ofs;
    ofs.open(argv[4], std::ofstream::out | std::ofstream::trunc);
    ofs<<argv[3]<<" "<<cost<<" "<<czas/CLOCKS_PER_SEC<<" ";
    for(int i = 0; i < cityamount; i++)
        ofs<<sequence[i]<<"->";
    ofs<<sequence[cityamount];
    ofs.close();
}

void writetab(int** cities)                 // wypisywanie aktualnej macierzy przejsc miedzy miastami
{
    std::cout << "\n\n";
    std::cout << cityamount << '\n';
    for(int i=0;i<cityamount;++i)
    {
        for(int j=0;j<cityamount;++j)
            std::cout<<cities[i][j]<<" ";
        std::cout<<"\n";
    }
}

void TabuSearch(int argc,char  *argv[])
{
    clock_t begin = clock();
    int iterationWoImprovement, maxIterationWoImprovement = atoi(argv[2]);    //okreslenie maksymalnej ilosci iteracji bez poprawy, po osiagnieciu ktorej program skonczy prace, jak rowniez deklaracja iteratora
    int tabuSize;      // ilosc przejsc zapamietanych w tabu
    if(atoi(argv[1]) > (cityamount-2)*(cityamount-2) / 2)
        { tabuSize = (cityamount-2)*(cityamount-2)/2; std::cout << "\nWielkosc tablicy Tabu poza zakresem, zmieniono ja na maksymalna dopuszczalna: " << tabuSize; }
    else tabuSize = atoi(argv[1]);
    int iteration = 0;              // iterator trzymajacy informacje o tym ile razy program wykonal algorytm

    int** tabuList = new int*[cityamount];             // inicjalizacja tablicy Tabu w rozmiarze x*x
    for(int i = 1; i < cityamount; i++)
        tabuList[i] = new int[cityamount];

    for(int i = 1; i < cityamount; i++)                 // pierwotne zerowanie tabu
        for(int j = 1; j < cityamount; j++)
            tabuList[i][j] = 0;

	int* bestPath = new int[cityamount + 1];      //sciezka i waga optymalnego rozwiazania
	int bestCost = std::numeric_limits<int>::max();

	int* tempBestPath = new int[cityamount + 1];  //sciezka i waga optymalnego rozwiazania tymczasowego
	int tempBestCost = std::numeric_limits<int>::max();
    tempBestPath[0] = tempBestPath[cityamount] = iterationWoImprovement = 0;

    int* tempPath = new int [2];                    // miasta aktualnie badanego sasiedztwa

    int bestResult = std::numeric_limits<int>::max();
    int tempCost = std::numeric_limits<int>::max();
    int tempV, temp = 0;

    bool* cityB = new bool[cityamount + 1];            //stworzenie tablicy mowiacej czy dana liczba juz wystapila w sekwencji
    cityB[0] = cityB[cityamount] = true;              //podpisanie pierwszego i ostatniego elementu jako juz wykonanego
    for(int i = 1; i < cityamount; i++)                 //podpisanie pozostalych jako niewykonanych
        cityB[i] = false;

    int amOfFailed = 0;
    for(int i = 1; i < cityamount; ++i)                // tworzenie pierwszej sekwencji, ustawienie pierwszego miasta jako poczatkowego i koncowego zostalo juz wykonane dlatego pomijamy
    {
        if(i < argc - amOfFailed - 4) // poczatkowa sekwencja miast zadeklarowana na wejsciu // -4 bo na wejsciu jest 5 arg zanim zaczniemy sekwencje, a iteracja zaczynana od 1
        {
            if(atoi(argv[i+amOfFailed+4]) <= 0 || atoi(argv[i+amOfFailed+4]) >= cityamount || cityB[atoi(argv[i+amOfFailed+4])] == true) // || isdigit(argv[i+amOfFailed+4])
            {
                std::cout << "\nPodano zly skladnik sekwencji, miasto: " << argv[i+amOfFailed+4] << " zostaje pominiete w sekwencji!";
                amOfFailed++;
                i--;
            }
            else
            {
                tempBestPath[i] = atoi(argv[i+amOfFailed+4]);
                cityB[atoi(argv[i+amOfFailed+4])] = true;
            }
        }
        else
        {
            tempV = std::numeric_limits<int>::max();
            for(int j = 1; j < cityamount; j++)
                if(cityB[j] == false && distances[tempBestPath[i-1]][j] < tempV){
                    tempV = distances[tempBestPath[i-1]][j];
                    temp = j;
                }
            cityB[temp] = true;
            tempBestPath[i] = temp;
        }
    }

    std::cout<<"\n\nStworzona sekwencja miast to:\n";           // wypisanie wynikow procesu na ekran
    for(int i = 0; i < cityamount; i++)
        std::cout << tempBestPath[i] << " -> ";
    std::cout << tempBestPath[cityamount] << "\n\n";

    tempBestCost = bestCost = 0;
    for(int i = 0; i < cityamount; i++)                 // obliczanie odleglosci nowej sciezki
        tempBestCost += distances[tempBestPath[i]][tempBestPath[i + 1]];

    bestCost = tempBestCost;                            // podpisanie jako najlepsza znaleziona
    for (int i = 0; i < cityamount + 1; i++)
        bestPath[i] = tempBestPath[i];


    do{
        iteration++;

        bestResult= std::numeric_limits<int>::max();
        for(int i = 1; i < cityamount-1; i++)
            for(int j = i+1; j < cityamount; j++){

                tempCost = 0;
                // wyliczanie roznicy w koszcie, obliczajac jedynie roznice miedzy sciezkami bedacymi czesciami zamienionych miast
                if(i+1 == j){
                    tempCost = distances[tempBestPath[i-1]][tempBestPath[j]] + distances[tempBestPath[j]][tempBestPath[i]] + distances[tempBestPath[i]][tempBestPath[j+1]] - distances[tempBestPath[i-1]][tempBestPath[i]] - distances[tempBestPath[i]][tempBestPath[j]] - distances[tempBestPath[j]][tempBestPath[j+1]];
//                        std::cout << "\n " << i << "  " << j << "  cost: " << tempCost << " = " << distances[tempBestPath[i-1]][tempBestPath[j]]  << " + " << distances[tempBestPath[j]][tempBestPath[i]] << " + " << distances[tempBestPath[i]][tempBestPath[j+1]] << " - " << distances[tempBestPath[i-1]][tempBestPath[i]] << " - " << distances[tempBestPath[i]][tempBestPath[j]] << " - " << distances[tempBestPath[j]][tempBestPath[j+1]];
                }
                else{
                    tempCost = distances[tempBestPath[i-1]][tempBestPath[j]] + distances[tempBestPath[j]][tempBestPath[i+1]] + distances[tempBestPath[j-1]][tempBestPath[i]] + distances[tempBestPath[i]][tempBestPath[j+1]] - distances[tempBestPath[i-1]][tempBestPath[i]] - distances[tempBestPath[i]][tempBestPath[i+1]] - distances[tempBestPath[j-1]][tempBestPath[j]] - distances[tempBestPath[j]][tempBestPath[j+1]];
//                        std::cout << "\n " << i << "  " << j << "  cost: " << tempCost << " = " << distances[tempBestPath[i-1]][tempBestPath[j]] << " + " << distances[tempBestPath[j]][tempBestPath[i+1]] << " + " << distances[tempBestPath[j-1]][tempBestPath[i]] << " + " << distances[tempBestPath[i]][tempBestPath[j+1]] << " - " << distances[tempBestPath[i-1]][tempBestPath[i]] << " - " << distances[tempBestPath[i]][tempBestPath[i+1]] << " - " << distances[tempBestPath[j-1]][tempBestPath[j]] << " - " << distances[tempBestPath[j]][tempBestPath[j+1]];
                }

//                    std::cout << "\n j: " << tempBestPath[j] << " i: " << tempBestPath[i];        //wypisywanie numerow zamienionych miast aby poprawnie uzyc tabuList
                if(tempBestPath[i] > tempBestPath[j]){                                          //tabuList dziala tylko po jednej stronie przekatnej macierzy przejsc, oby oszczedzic na ilosci operacji. wybieramy te strone realizujac podanego ifa
//                        std::cout << "  j < i";
                    if(tabuList[tempBestPath[j]][tempBestPath[i]] < iteration){      //sprawdzenie czy wygenerowany sasiad nie nalezy do tabu lub spelnia kryterium aspiracji
                        if(tempCost < bestResult){                                             //sprawdzenie czy wygenerowany sasiad jest lepszy od juz sprawdzonych
                            tempPath[0] = i;
                            tempPath[1] = j;
                            bestResult = tempCost;
                    }    }
                }
                else{                                                                           //to samo co w if z ta roznica, ze zostala wybrana komorka tablicy znajduja sie symetrycznie do przekatnej macierzy, aby uzywac tylko polowy tablicy
//                        std::cout << "  j > i";
                    if(tabuList[tempBestPath[i]][tempBestPath[j]] < iteration)
                        if(tempCost < bestResult){
                            tempPath[0] = i;
                            tempPath[1] = j;
                            bestResult = tempCost;}
                }
            }

        temp = tempBestPath[tempPath[0]];                               //zamiana najlepszych miast miejscami
        tempBestPath[tempPath[0]] = tempBestPath[tempPath[1]];
        tempBestPath[tempPath[1]] = temp;

//            std::cout << "\n\n";                                        //sprawdzanie nowej, najlepszej sciezki
//            for(int i = 0; i < cityamount; i++)
//                std::cout << tempBestPath[i] << " -> ";
//            std::cout << tempBestPath[cityamount] << "  tempBestCost: " << tempBestCost << "\n zamiana miejsca: " << tempPath[0] << " z " << tempPath[1];

//        temp = 0;
//        for(int i = 0; i <cityamount; i++)
//            temp += distances[tempBestPath[i]][tempBestPath[i + 1]];
//            std::cout << "   Wyliczony nowy koszt: " << temp;         //wypis kosztu nowej sciezki

//            tempBestCost = temp;
        tempBestCost += bestResult;


        if(tempBestPath[tempPath[0]] < tempBestPath[tempPath[1]])                           // dodanie nowego przejscia do tabuList o wartosci iteration + tabuSize, czyli aktualnego numeru przejscia plus ile jeszcze dana rzecz ma pozostac w tabu
            tabuList[tempBestPath[tempPath[0]]][tempBestPath[tempPath[1]]] = tabuSize + iteration;
        else
            tabuList[tempBestPath[tempPath[1]]][tempBestPath[tempPath[0]]] = tabuSize + iteration;


//        std::cout << "\n\n";
//        for(int i = 1; i < cityamount; i++){               // wypisanie tabuList
//            for(int j = 1; j < cityamount; j++){
//                std::cout << tabuList[i][j] << " ";}
//           std::cout << "\n";}

        if( bestCost > tempBestCost)                    //zapisanie nowego najlepszego wyniku, badz zaznaczenie kolejnego z rzedu przejscia petli bez niego, aby wywolac funkcje dywersyfikacji
        {
            bestCost = tempBestCost;
            iterationWoImprovement = 0;
            for (int i = 0; i < cityamount + 1; i++)
                bestPath[i] = tempBestPath[i];
        }
        else
            iterationWoImprovement++;


//        std::cout<< "\n" << tempPath[0] << " " << tempPath[1];        // wypis zamienianych miast

    }while(iterationWoImprovement < maxIterationWoImprovement);

    std::clock_t end = clock();
    double czas = end - begin;
    std::cout<<"\nCzas: " << czas / CLOCKS_PER_SEC;

    std::cout << "\n" << iteration << "  " << bestCost << "\n";
//    std::cout<<"\n\nNajkrotsza odnaleziona droga przez wszystkie miasta to:\n";           // wypisanie wyników procesu na ekran
    for(int i = 0; i < cityamount; i++)
        std::cout << bestPath[i] << " -> ";
    std::cout << bestPath[cityamount];
//    std::cout<<"\nJej calkowity dystans wynosi: " << bestCost;

    if(result(bestCost, argv) == 1){
        std::cout<<"\nPrzekazujemy wynik";
        filewrite(bestPath, bestCost, argv, czas);
    }

 /*   for(int i = 0; i < cityamount; i++){
    	std::cout << "Wywalam: "<< i << "\n";
        delete[] tabuList[i];
    }*/
    delete[] tabuList;
    delete[] tempBestPath;
	delete[] bestPath;
    delete[] tempPath;
    delete[] cityB;
}
