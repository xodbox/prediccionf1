from collections import namedtuple

limitetiempo = 4

Piloto = namedtuple('Piloto', ['orden', 'numero', 'nombre', 'apellido', 'escuderia', 'abreviacion'])

pilotos = [
			Piloto(1, 44, "Lewis", "Hamilton", "Mercedes", "HAM(Mer)"),
			Piloto(2, 6, "Nico", "Rosbeg", "Mercedes", "ROS(Mer)"),
			Piloto(3, 5, "Sebastian", "Vettel", "Ferrari", "VET(Fer)"),
			Piloto(4, 7, "Kimi", "Raikkonen", "Ferrari", "RAI(Fer)"),
			Piloto(5, 19, "Felipe", "Massa", "Williams", "MAS(Wil)"),
			Piloto(6, 77, "Valtteri", "Bottas", "Williams", "BOT(Wil)"),
			Piloto(7, 3, "Daniel", "Ricciardo", "Red Bull", "RIC(RdB)"),
			Piloto(8, 33, "Max", "Verstappen", "Red Bull", "VER(RdB)"),
			Piloto(9, 11, "Sergio", "Perez", "Force India", "PER(FoI)"),
			Piloto(10, 27, "Nico", "Hulkenberg", "Force India", "HUL(FoI)"),
			Piloto(11, 20, "Kevin", "Magnussen", "Renault", "MAG(Ren)"),
			Piloto(12, 30, "Jolyon", "Palmer", "Renault", "PAL(Ren)"),
			Piloto(13, 26, "Daniil", "Kvyat", "Toro Rosso", "KVY(ToR)"),
			Piloto(14, 55, "Carlos", "Sainz", "Toro Rosso", "SAI(ToR)"),
			Piloto(15, 9, "Marcus", "Ericsson", "Sauber", "ERI(Sau)"),
			Piloto(16, 12, "Felipe", "Nasr", "Sauber", "NAS(Sau)"),
			Piloto(17, 14, "Fernando", "Alonso", "McLaren", "ALO(McL)"),
			Piloto(18, 22, "Jenson", "Button", "McLaren", "BUT(McL)"),
			Piloto(19, 8, "Romain", "Grosjean", "Hass", "GRO(Has)"),
			Piloto(20, 21, "Esteban", "Gutierrez", "Hass", "GUT(Has)"),
			Piloto(21, 94, "Pascal", "Wehrlein", "Manor", "WEH(Man)"),
			Piloto(22, 88, "Rio", "Haryanto", "Manor", "HAR(Man)")
			]
