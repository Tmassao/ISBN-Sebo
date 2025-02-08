from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup

def buscar_preco_estante_virtual(isbn):
    """Busca o menor preço do livro na Estante Virtual pelo ISBN."""
    url = f"https://www.estantevirtual.com.br/busca?q={isbn}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return "Erro ao acessar a Estante Virtual"

    soup = BeautifulSoup(response.text, "html.parser")
    precos = soup.find_all("span", class_="price")

    if not precos:
        return "Livro não encontrado"

    lista_precos = [float(preco.text.replace("R$", "").replace(",", ".")) for preco in precos]
    return f"R$ {min(lista_precos)}" if lista_precos else "Nenhum preço encontrado"

class ISBNScannerApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)
        self.label = Label(text="Pressione o botão para escanear o ISBN", size_hint=(1, 0.2))
        self.button = Button(text="Escanear ISBN", size_hint=(1, 0.2), on_press=self.scan_isbn)

        layout.add_widget(self.label)
        layout.add_widget(self.button)
        return layout

    def scan_isbn(self, instance):
        cap = cv2.VideoCapture(0)  # Ativa a câmera

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            for barcode in decode(frame):
                isbn = barcode.data.decode('utf-8')
                cap.release()
                preco = buscar_preco_estante_virtual(isbn)
                self.label.text = f"ISBN: {isbn}\nPreço: {preco}"
                return

        cap.release()
        self.label.text = "Nenhum ISBN detectado."

if __name__ == "__main__":
    ISBNScannerApp().run()
