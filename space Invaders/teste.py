
import Cliente.py
import threading



i = 0
def test_connections():
	while True:
		print("tentando conectar")
		c = threading.Thread(target = Cliente.py)
		c.start()
		print("Thread "+i+" criada")
		i+=1
			


print("tentando conexao")
test_connections()
