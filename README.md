# imageCombining
This is a python program to add many tiny photo tiles to make it look like a large photo, so-called mosaic-style.
I mainly used the PIL library to process the photos, calculating each small tile's average RGB value, spliting the large photo into tiny tiles and also calculating the average value. Then compare their difference (Euclid distance) to find the optimistic small tile that can fit.
