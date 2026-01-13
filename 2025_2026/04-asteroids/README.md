Szuflada/AM/Asteroid_Physics_lab/data - pliki 
Aspect data - S-A [au], E-A[au], alpha, lambda, beta
julian date, brightness
moja planetoida - 907 Rhoda
otwieramy plik ATL
robimy tabele z datą obserwacji (observing time to co jest w nawiasie) oraz aspect data: 3 kolumna (alfa) i 4 kolumna (lambda)
robimy podział w stosunku do lambdy (tak, żeby np nie było różnicy pomiędzy nimi o 20 stopni) to jest jeden punkt
tworzymy wykres polarny z

Planetoidy są w Szuflada/Asteroid_Physics_lab/data
tworzymy wykres polarny z opozycjami. 1 Opozycja jest jak alpha i lambda nie zmieniają się o max 20 stopni - widać po datach 
 
Liczymy okres rotacji w katpadzie, ale najpierw edytujemy w pliku .bashrc na samym dole od “conda_setup (..)” do “unset __conda_setup” - - - > musimy odznaczyć, żeby działało. 
żeby włączyć kat_pada musimy jeszcze w konsoli wpisać export TERM=v100 
w katpadzie (który jest w folderze razem z naszym plikiem ATL) wpisujemy ./ numer planetoidy i najpierw szukamy okresu rotacji dla naszej planetoidy (mi się nie chciało, znalazłam sobie jaki moja ma) i określamy dla każdej opozycji z dokładnością 0.001 
Tworzymy wykres (templatka jest gdzieś tam w folderze), możesz w pythonie, nikt ci nie zabroni, ale trzeba uwzględnić wszystko co tam jest 
trzeba mieć dwa wykresy, ale liczymy dla każdej opozycji, bo ważny jest zakres rotacji 

na razie tyle
sprawdzamy czy w ATL są obserwacje z Tess albo Kepler
