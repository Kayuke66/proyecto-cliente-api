from api_client.digital_twin import digital_twin_tree

def main():
    datos = digital_twin_tree()

    if datos is None:
        print("No ha sido posible obtener los datos.")
    elif not datos:
        print("La API responde, pero no hay datos aún")
    else:
        print("Datos recibidos:")
        print(datos)

if __name__ == "__main__":
    main()