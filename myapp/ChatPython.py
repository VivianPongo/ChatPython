import flet as ft

class Mensaje():
    def __init__(self, nombre_usuario:str, texto: str, tipo_mensaje:str):
        self.nombre_usuario = nombre_usuario
        self.texto = texto
        self.tipo_mensaje = tipo_mensaje

class Chat_Mensaje(ft.Row):
    def __init__(self, mensaje: Mensaje):
        super().__init__()
        self.vertical_alignment = "start"
        self.controls=[
            ft.CircleAvatar(
                content=ft.Text(self.get_iniciales(mensaje.nombre_usuario)),
                color=ft.colors.WHITE,
                bgcolor=self.get_avatar_color(mensaje.nombre_usuario)
            ),

            ft.Column(
                [
                    ft.Text(mensaje.nombre_usuario, width="bold"),
                    ft.Text(mensaje.texto, selectable=False),
                ],
                tight=True,
                spacing=5

            ),
        ]
    
    def get_iniciales(self, nombre_usuario:str):
        if nombre_usuario:
            return nombre_usuario[:1].capitalize()
        else:
            return "Unknown"

    def get_avatar_color(self, nombre_usuario:str):
        colores_avatar = [
            ft.colors.AMBER,
            ft.colors.BLUE,
            ft.colors.BROWN,
            ft.colors.CYAN,
            ft.colors.GREEN,
            ft.colors.INDIGO,
            ft.colors.LIME,
            ft.colors.ORANGE,
            ft.colors.PINK,
            ft.colors.PURPLE,
            ft.colors.RED,
            ft.colors.TEAL,
            ft.colors.YELLOW,
        ]
        return colores_avatar[hash(nombre_usuario)% len(colores_avatar)]



def main(page: ft.Page):
    page.horizontal_alignment = "stretch"
    page.title = "Flet Python Chat :D"

    def unirse_al_chat_click(e):
        if not nombre_usuario_unido.value:
            nombre_usuario_unido.error_text = "El nombre no puede estar en blanco",
            nombre_usuario_unido.update()
        else:
            page.session.set("user_name", nombre_usuario_unido.value)
            page.dialog.open = False
            nuevo_mensaje.prefix = ft.Text(f"{nombre_usuario_unido.value}: ")
            page.pubsub.send_all(Mensaje(nombre_usuario=nombre_usuario_unido.value, 
                                         texto=f"{nombre_usuario_unido.value} se ha unido al chat", 
                                         tipo_mensaje="login_mensaje"))
            #aumentamos el resto
            page.update()
    
    def enviar_mensaje_click(e):
        if nuevo_mensaje.value != "":
            page.pubsub.send_all(Mensaje(page.session.get("user_name"), 
                                         nuevo_mensaje.value, 
                                         tipo_mensaje="chat_mensaje"))
            nuevo_mensaje.value = ""
            nuevo_mensaje.focus()
            page.update()
        

    def on_message(mensaje:Mensaje):
        if mensaje.tipo_mensaje == "chat_mensaje":
            m = Chat_Mensaje(mensaje)
        elif mensaje.tipo_mensaje=="login_mensaje":
            m=ft.Text(mensaje.texto, italic=True, color=ft.colors.GREY, size=12)
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

 #para pedir el nombre del usuario
    nombre_usuario_unido = ft.TextField(
        label="Ingresa tu nombre para unirte al chat",
        autofocus= True,
        on_submit=unirse_al_chat_click
    )

    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Bienvenido!"),
        content=ft.Column(
            [nombre_usuario_unido],
            width=300,
            height=70,
            tight=True
        ),
        actions=[ft.ElevatedButton(
            text="Unirse al Chat",
            on_click=unirse_al_chat_click
        )],
        actions_alignment="end",
    )
    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    nuevo_mensaje=ft.TextField(
        hint_text="Escribe un mensaje...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=enviar_mensaje_click,
    )


    page.add(
        ft.Container(
            content=chat,
            border=ft.border.all(1,ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True
        ),
        ft.Row(
            [
                nuevo_mensaje,
                ft.IconButton(
                    icon=ft.icons.SEND_ROUNDED,
                    tooltip="Send message",
                    on_click=enviar_mensaje_click,
                ),

            ],
           
        ),


        ft.Text("Hola mundo", size=20)
    )



ft.app(port=8550, target = main, view=ft.AppView.WEB_BROWSER)