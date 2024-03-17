#pip install flet
#flet create myapp
import flet as ft

#PubSub --> mechanism for asynchronous communication between page sessions
#First, we need subscribe the USER to receive broadcast messages
class Mensaje():
    def __init__(self, user:str, text:str, tipo_mensaje:str):
        self.user = user
        self.text = text
        self.tipo_mensaje = tipo_mensaje #diferenciar mensaje de entrar al login y chat normal


def main(page: ft.Page):
    chat = ft.Column()
    nuevo_mensaje = ft.TextField(
        bgcolor=ft.colors.GREY,
        filled=True,
        hint_text="Enter message here",
        border=ft.InputBorder.NONE, 
        color=ft.colors.BLACK,
        hint_style= {"font-size": 20.0, "color": ft.colors.TERTIARY}

    )

    def on_message(mensaje: Mensaje):
        #dentro de la columna de chat colocar
        #mensaje es de la clase mensaje y tiene un usuario y texto
        if mensaje.tipo_mensaje == "chat_mensaje":
            chat.controls.append(
                ft.Text(f"{mensaje.user}: {mensaje.text}")
            )
        elif mensaje.tipo_mensaje == "login_mensaje":
            chat.controls.append(
                ft.Text(mensaje.text, italic=True, color=ft.colors.ORANGE, size=12)
            )
        
        page.update()

    #mensajes en tiempo real
    page.pubsub.subscribe(on_message)

    user_name = ft.TextField(
        label="Ingresa tu nombre de usuario", color=ft.colors.BLACK, 
        border=ft.InputBorder.NONE, 
        bgcolor=ft.colors.WHITE70,
        filled=True,
        hint_text="Escriba su nombre aquí"
    )


    def enviar_click(e):
        page.pubsub.send_all(
            Mensaje(user=page.session.get("user_name"), text=nuevo_mensaje.value, tipo_mensaje="chat_mensaje")

        )
        nuevo_mensaje.value = "" #se borra el mensaje value al enviar el mensaje para colocar otro nuevo
        page.update()

    def join_clicked(e):
        if not user_name.value:
            user_name.error_text = "El nombre no puede estar en blanco"
            user_name.update()

        else:
            page.session.set("user_name", user_name.value)
            page.dialog.open = False
            page.pubsub.send_all(
                Mensaje(user=user_name.value, text=f"{user_name.value} se ha unido al chat.", tipo_mensaje="login_mensaje")
            )
            page.update()

    
    page.dialog = ft.AlertDialog(
        open= True,
        modal=True,
        title=ft.Text("Bienvenido!"),
        content=ft.Column(
            [user_name],
            tight=True
        ),
        actions=[
            ft.ElevatedButton(text="Unirse al chat", on_click=join_clicked)
        ],
        actions_alignment= "end",
    )


    page.add(
        chat, 
        ft.Row(
            controls=[
                nuevo_mensaje,
                ft.ElevatedButton("Send", on_click=enviar_click)
            ]
        )
    )

#If you open this app in two web browser tabs, it will create two app sessions. Each session will have its own list of messages.
ft.app(main, view=ft.AppView.WEB_BROWSER)
