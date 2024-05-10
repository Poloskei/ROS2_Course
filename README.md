A projekt szokásos ros2 környezetben készült a turtlesim node-ját felhasználva rajzol ki Koch fraktálokat. A program rekurzívan hív meg külön egyenesen mozgató, és forduló függvényeket.
  Az alapvető v=s/t számítás helyett a teknőst arányosan szabályozzuk, úgy, hogy a megtenni kívánt távolságot az eddig megtetthez hasonlítjuk. Ehhez elmentjük a kiindulási pontot. A sebességet a célhoz közeledve arányosan csökkentjük. 
Viszont, hogy ne legyen túl lassú 0.1 alatti különbségnél már nem csökkentjük tovább, ezzel egy minimális hibát engedélyezve.
  A fordulás hasonló elven működik, itt viszont sokkal könnyebb kiszámítani a mozgás célpontját. A kezdeti thetából kivonva a kívánt szög radiánját az eredmény megadja, hogy milyen irányba kell fordulni. Itt is folyamatosan lassul a mozgás a célhoz közeledve.
A program képes túlfordulni a szögön, ezért a differencia szöget minden lefutáskor vizsgáljuk, és beállítjuk a kívánt -π és π közé. A különbség abszolut értékét vizsgálva a program képes korrigálni a túlfordulást.
A sebesség növelése érdekében megengedünk egy 0.0002-es eltérést.
