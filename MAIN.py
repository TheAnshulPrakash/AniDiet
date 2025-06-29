import flet as ft
import threading
import ollama
import asyncio
import Conv


def convo(container : ft.Container, text, col):
    
    
    history =[]
    col.controls.append(
            ft.Text(f"You: {text}",color="#f0ad6f", size=20)
        )
    container.update()
    async def send_message():
        if text.lower() in ['exit', 'quit']:            
            return

        history.append({'role': 'user', 'content': text})

        
        
        ai_typing = ft.Text("AniDiet: \n", color="black", size=13)
        col.controls.append(ai_typing)
        container.update()

        full_reply = ""
        stream = ollama.chat(model='mistral', messages=history, stream=True)

        for chunk in stream:
            content = chunk['message']['content']
            for char in content:
                full_reply += char
                ai_typing.value = f"AniDiet: {full_reply}"
                container.update()
                await asyncio.sleep(0.01)

        
        col.controls.remove(ai_typing)
        col.controls.append(
            ft.Markdown("AniDiet: "+full_reply, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, )
        )
        
       
        div=ft.Divider(thickness=1, color="#f9cca2", leading_indent=20, trailing_indent=20, height=50)
        col.controls.append(div)
        history.append({'role': 'assistant', 'content': full_reply})
    container.content=col
    container.alignment=ft.alignment.top_left
    container.expand=True
    asyncio.run(send_message())
    container.update()
    


def main(page: ft.Page):
    
    
    page.theme_mode = "light"
    page.scroll="auto"
    
    page.fonts={
        "Baloo": "fonts/Baloo2-Regular.ttf"
    }
    
    page.theme = ft.Theme(font_family="Baloo")
    

    
    
    
    image_op=ft.Image("images/anime_chef.png", fit=ft.ImageFit.CONTAIN, height=500, expand=True, width=500)
    image_ed=ft.Image("images/anime_nurse.png", fit=ft.ImageFit.CONTAIN, height=500,  expand=True, width=500)
    image_logo=ft.Image("images/logo.png", height=100,width=100, fit=ft.ImageFit.CONTAIN)
    
    
    image_result=ft.Image("images/anime_result.png", fit=ft.ImageFit.CONTAIN, height=500,  width=500)
    
    image_ai=ft.Image("images/anime_ai.png", fit=ft.ImageFit.CONTAIN, height=500,  width=500)
    
    
    handle_ref=ft.Ref[ft.TextField]()
    
    
    
    user=""
    user_friends=[]
    def on_login(e):
        
        nonlocal user
        user = handle_ref.current.value
        user_data=Conv.from_firebase(user)
        if user_data!=None:
            if user_data.get('age')!=None:
                age_dropdown.value=user_data['age']
            veg_only.value=user_data['Vegetarian']
            if user_data.get('gender')!=None:
                gender_options.value=user_data['gender']
            nonlocal streak
            streak = user_data['streak']
            streak_ref.current.value=f"Your streak: {streak} days!🔥"
            streak_ref.current.update()
            
            if user_data.get('goals')!=None:
                selected_tiles=user_data['goals']
            if user_data.get('friends')!=None:
                nonlocal user_friends
                user_friends=user_data['friends']
                
            
                print("selected tiles are", selected_tiles)
                for string in selected_tiles:
                    if string=="Glowing Skin": glow_skin.bgcolor='#ffe0c0'
                    if string=="Gain Weight": weight_gain.bgcolor='#ffe0c0'
                    if string=="Lose Weight": weight_lose.bgcolor='#ffe0c0'
                    if string=="Muscle Gain": muscle_gain.bgcolor='#ffe0c0'
                    
            if user_data.get('plan')!=None:
                result_container.height=400
                result_container.scale=ft.Scale(1)
                col2.controls.append(
                    ft.Markdown("\n\n"+user_data['plan'], selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, )
                )
                result_diet.content=col2
                
                result_diet.update()
            
          
            
        page.close(login_dialog)
        user_name_ref.current.value=f"Hi @{user}"
        user_name_ref.current.size=35
        user_name_ref.current.update()
        print(user)
        
        page.update()
    
    
    login_container=ft.Container(
        
        ft.Column([
            ft.Column([
            ft.Row([
                ft.Text("Start your arc!", size=25, color="#f9cca2"), ft.Image("images/anime_new_user.png", height=50, width=50, fit=ft.ImageFit.CONTAIN)
            ]),
            ft.Row([
                ft.Text("Or Continue it!", size=25, color="#f9cca2"), ft.Image("images/anime_old_user.png", height=50, width=50, fit=ft.ImageFit.CONTAIN)
            ])]),
            
            
        ft.Row([
            ft.Text("User Tag", size=20),ft.TextField(hint_text="Enter your @handle", width=200, border_color="#f9cca2", color="#5c6262", ref=handle_ref)
            
            ],
               vertical_alignment=ft.CrossAxisAlignment.CENTER
               
               
            
        ),
        ft.Row([
            ft.CupertinoButton("Cancel", bgcolor="#f9cca2", color="white", width=120,), 
            ft.CupertinoButton("Go!", bgcolor="#f9cca2", color="white", width=70, on_click=lambda e: on_login(e))
        ], alignment=ft.MainAxisAlignment.END)
        ,
                  ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        
        
        padding=ft.Padding(30,10,10,10),
        height=350,
        width=400,
        border_radius=20,
        border=ft.border.all(5, "#f9cca2"),
        
        bgcolor="#ffffff",
        expand=True
    )
    
    
    
        
    
    login_dialog=ft.AlertDialog(
        title="Login!",
        title_text_style=ft.TextStyle(color="#f9cca2", size=30),
       
        content=login_container,
       
        visible=False,
        bgcolor='white',
    )
    
    def login(e):
        print(e.name)
        
        
        login_dialog.visible=True
        e.control.page.overlay.append(login_dialog)
        login_dialog.open=True
        e.control.page.update()
        age_dropdown.value=None
        gender_options.value=None
        
        print(user)
        
    user_name_ref=ft.Ref[ft.Text]()
    
    headline_row = ft.Stack(
        [
            ft.Row(
                [
                    image_logo,
                    ft.Text("AniDiet", size=30, weight=ft.FontWeight.BOLD, color="#f0ad6f")
                ],
                height=100,
                expand=False,
                left=50,
            ),
            
            ft.Row(
                [   ft.Text("Login to unlock all features", size=16,  color="#f0ad6f", ref=user_name_ref),
                    ft.IconButton(icon=ft.Icons.LOGIN_ROUNDED, icon_size=40, tooltip="Login", icon_color="#f0ad6f", on_click=login)
                ],
                
                alignment=ft.MainAxisAlignment.END,
                right=40,
                width=1000,
                spacing=10
            )
        ],
        height=100,
        expand=True
        )
    
    
    age_options = ["1-5 years"] + ["6-10 years"] + ["11-15 years"] + ["16-20 years"] + ["21-25 years"] + ["26-30 years"] + ["31-35 years"] + ["36-40 years"] + ["41-45 years"] + ["46-50 years"] + ["51-55 years"] + ["56-60 years"] + ["61-65 years"] + ["66-70 years"] + ["70+ years"]
    age_dropdown = ft.Dropdown(
        label="Select your age",
        width=300,
        options=[ft.dropdown.Option(value) for value in age_options]
    )
    label_gender= ft.Text("Select your gender:", size=20)
    gender_options = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Male", label="Male", fill_color="#F0AD6F"),
            ft.Radio(value="Female", label="Female", fill_color="#F0AD6F"),
            ft.Radio(value="Rather not say", label="Rather not say", fill_color="#F0AD6F"),
        ],alignment=ft.MainAxisAlignment.CENTER )
    )
    
    label_goals= ft.Text("Choose your diet goals🎯", size=20)
    
    
    selected_tiles= []
    streak=0
    
    def create_tile(title, description=None):
        tile = ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD),
                ft.Text(description)
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            margin=10,
            width=250,
            border_radius=12,
            border=ft.border.all(1, ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            ink=True,
            animate=ft.Animation(500, "easeInOut")
        )

        def toggle_selection(e):
            if title in selected_tiles:
                selected_tiles.remove(title)
                tile.bgcolor = ft.Colors.WHITE
            else:
                selected_tiles.append(title)
                tile.bgcolor = "#ffe0c0"
            tile.update()
            

        tile.on_click = toggle_selection

        tile.on_hover = lambda e: (
            setattr(tile, "shadow", ft.BoxShadow(blur_radius=30,  color="#f0ad6f") if e.data == "true" else ft.BoxShadow(blur_radius=0, color="#f9cca2")),
            tile.update()
        )

        return tile
    
    full_reply=""
    def on_plan_done(e):
        print(gender_options.value)
        print(age_dropdown.value)
        print(selected_tiles)
        text =f"Create a daily diet planner for {age_dropdown.value}, {gender_options.value} planning {selected_tiles} {fine_tuning.value} "
        if veg_only.value:
            print(veg_only.label)
            text +=veg_only.label
            
        page.close(details)
        
        
        
        print(text)
        result_container.height=400
        result_container.scale=ft.Scale(1)
        
        result_container.update()
        
        def diet_planner(container: ft.Container, text, col):
            
            container.height = 400
            history=[]
            async def send_message():
                

                history.append({'role': 'user', 'content': text})

            
                
                ai_typing = ft.Text("", color="black", size=13)
                col.controls.append(ai_typing)
                container.update()

                nonlocal full_reply
                stream = ollama.chat(model='mistral', messages=history, stream=True)

                for chunk in stream:
                    content = chunk['message']['content']
                    for char in content:
                        full_reply += char
                        ai_typing.value = f"{full_reply}"
                        container.update()
                        await asyncio.sleep(0.005)

                
                col.controls.remove(ai_typing)
                
                col.controls.append(
                    ft.Markdown("\n\n"+full_reply, selectable=True, extension_set=ft.MarkdownExtensionSet.GITHUB_WEB, )
                )
            
            container.content=col
            container.alignment=ft.alignment.top_left
            container.update()
            
            asyncio.run(send_message())
        diet_planner(result_diet,text,col2)
        #threading.Thread(target=diet_planner, args=(result_diet,text,col2,)).start()
        
        
    glow_skin = create_tile("Glowing Skin", description="Nourish your skin from within with a glow-enhancing diet. ✨")
    weight_gain = create_tile("Gain Weight", description="Follow a balanced plan to gain weight safely and effectively. ⚖️")
    weight_lose = create_tile("Lose Weight", description="Adopt a sustainable strategy to shed excess weight healthily. 🏃‍♂️")
    muscle_gain = create_tile("Muscle Gain", description="Build strength and lean muscle with a tailored nutrition plan. 💪")
    
    tiles=ft.Row([glow_skin, weight_gain, weight_lose, muscle_gain], wrap=True)
    
    veg_only= ft.CupertinoSwitch(
        label="Vegetraian",
        value= False,
        active_color= "#76ce5f",
        label_position=ft.LabelPosition("left")
        
    )
    
    fine_tuning=ft.TextField(
        hint_text="What should we keep in mind when planning your diet?", width=520, border_color='#f9cca2', cursor_color="#5c6262", color="#5c6262"
        
        )
    
    details_container=ft.Container(
        ft.Column([
        ft.Column([age_dropdown,
                   ft.Row([ft.Row([label_gender,gender_options]), veg_only], vertical_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                   label_goals, tiles, fine_tuning
             
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                  expand=True, spacing=10, scroll="auto",),
        ft.CupertinoButton("Go!", bgcolor="#f9cca2", color="white", width=70, on_click=on_plan_done)], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        height=500,
        width=700,
        border_radius=20,
        padding=ft.Padding(25,40,25,25),
        border=ft.border.all(5, "#f9cca2"),
        margin=ft.Margin(0,10,0,0),
        
        
        bgcolor="#ffffff",
        expand=True
    )
    
    
    details=ft.AlertDialog(
        title="Enter your details here. \nOur model will craft a personalized diet for you",
        content=details_container,
       
        visible=False,
        bgcolor='#ffffff',
        
        
    )
    def get_started(e):
        details.visible = True
        e.control.page.overlay.append(details)
        details.open = True
        e.control.page.update()
        details.update()
        page.update()

    
    

    
    
    result_diet=ft.Container(
        
        
        height=400,
        expand=True,
        bgcolor="#ffffff",
        
        
        
    )
    def save_planner(e):
        
        if user!="":
            user_data={
                'handle':user,
                'age':age_dropdown.value,
                'gender':gender_options.value,
                'Vegetarian':veg_only.value,
                'goals':selected_tiles,
                'plan':full_reply,
                'streak':streak
            }
            Conv.to_firebase(user_data)
        else:
            login(e)
       
    
    def streak_count_add(e):
        nonlocal streak
        streak_count.label="Well done, you're one step closer to achieveing your goals"
        streak_count.disabled=True
        streak+=1
        streak_ref.current.value=f"Your streak: {streak} days 🔥!"
        streak_ref.current.update()
        
        
        temp_data={
            'handle':user,
            'streak':streak
        }
        Conv.to_firebase(temp_data)
        streak_count.update()
    streak_count=ft.CupertinoCheckbox(label="Did you finish the plan today?", value=False, on_change=streak_count_add)
    
    
    result_diet_cover=ft.Container(
        content=ft.Column([
            result_diet,
            ft.Row([streak_count,
            ft.Row([ft.CupertinoButton("Tune it!", bgcolor="#f9cca2", color="white", on_click=get_started),
                    ft.CupertinoButton("Save", bgcolor="#f9cca2", color="white",  on_click=save_planner)], 
                   alignment=ft.MainAxisAlignment.END)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ]),
        border=ft.border.all(10,"#f9cca2"),
        height=400,
        expand=True,
        bgcolor="#ffffff",
        border_radius=30,
        padding=ft.Padding(20,20,20,20)
        
    )
    
    result_container=ft.Container(
        ft.Row([image_result, result_diet_cover]),
        
        
        
        
        height=0,
        expand=True,
        
        
        scale=ft.Scale(0),
        animate_scale=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
        padding=ft.Padding(0,5,5,5),
        
        border_radius=30,
        margin=ft.Margin(0,0,50,0),
        
        
        
    )
    
    result_row=ft.Row([
        result_container
    ], expand=True, alignment=ft.MainAxisAlignment.CENTER)
    
    
    plan_container=ft.Container(
        ft.Column([
                    ft.Text("Create Your Diet Plan", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                    ft.Text("Our agentic AI will help you plan a personalized diet.", size=16, text_align=ft.TextAlign.CENTER,color="#5c6262"),
                    ft.CupertinoButton("Get Started", bgcolor="#f9cca2", color="white", width=150, on_click=get_started)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        height=450,
        width=450,
        border_radius=450,
        bgcolor="#ffffff",
        border=ft.border.all(10, "#f9cca2"),
        expand=True
        
    )
    title_row = ft.Column([
            ft.Row([
                image_op,
                plan_container,
                image_ed
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        ], alignment=ft.MainAxisAlignment.START)  
      
    title_container_ref=ft.Ref[ft.Container]()
    
    
    
    title_container=ft.Container(
        title_row,
        ref=title_container_ref,
        
        
        
        padding=ft.Padding(0, 40, 20, 40),
        margin=0,
        border_radius=25,  
        expand=True,
        height=500             
        
    )
    
    
    
    div1=ft.Divider(thickness=1, color="#f9cca2", leading_indent=100, trailing_indent=100, height=50)
    
    send_message=ft.TextField(hint_text="Message to get started",expand=True, height=50, border_color="#f9cca2", border_radius=30, 
                    content_padding=ft.Padding(left=20,top=0,right=0,bottom=30), cursor_color="#5c6262", color="#5c6262")
    
    col=ft.Column([ft.Row(expand=True)],scroll="auto", expand=True, auto_scroll=True)
    
    col2=ft.Column([ft.Row(expand=True)],scroll="auto", expand=True, auto_scroll=True)
    
    
    def send_button_clicked(e):
        
        
        
        text=send_message.value
        print(text)
        threading.Thread(target=convo, args=(message_container,text,col,)).start()
        send_message.value=""
        send_message.update()
        
        message_container.alignment=ft.alignment.top_left
        message_container.expand=True
        
        
        message_container.padding=ft.Padding(20,15,20,10)
        
        
        
       
        
        
        
        message_container.update()
    
    send_button=ft.IconButton(icon=ft.Icons.SEND_ROUNDED, icon_color="#f9cca2", icon_size=45, on_click=send_button_clicked)
    
    null_message=ft.Text("Ready when you are!", size=25,text_align=ft.TextAlign.CENTER, expand=True)
    
    message_ref=ft.Ref[ft.Container]()
    message_container=ft.Container(
                    null_message,
                    alignment=ft.alignment.center,
                    expand=True,
                    ref=message_ref,
                    height=20,
        
                )
    ai_text_box=ft.Container(
        content=ft.Column(
            controls=[
                message_container,
                ft.Container(
                    ft.Row([send_message, send_button]),
                    alignment=ft.alignment.bottom_center
                ),
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            
        ),

            height=500,
            expand=True,
            padding=ft.Padding(20,5,5,5),
            
            border=ft.border.all(10, "#f9cca2"),
            border_radius=30,
            bgcolor="#ffffff",
            margin=ft.Margin(50,0,0,0),
            
            
        )
        
    
    conversation_container=ft.Container(
        ft.Row([
            ai_text_box, image_ai
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,vertical_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
        height=500,
        
        
    )
    
    
    ai_line=ft.Column([
        ft.Row([
        ft.Text("Have a doubt regarding diet or need recepies?", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#f0ad6f", expand=True)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([ft.Text("Ask me anything", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, color="#f0ad6f"),
        ft.Image("images/anime_ricecake.png", height=50, width=50)],alignment=ft.MainAxisAlignment.CENTER)
        
    ], alignment=ft.CrossAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    
    
    
    friends_input=ft.TextField(hint_text="Enter your friend's @handle", border_color='#f9cca2', cursor_color='#5c6262', border_width=3, hint_fade_duration=400, autofill_hints=False,)
    
    

        
    data_table = ft.DataTable(
        sort_column_index=1,
        sort_ascending=False,
        columns=[
            ft.DataColumn(label=ft.Text("")),
    
            ft.DataColumn(label=ft.Text("Streak days")),
        ],
        width=450,
        rows=[]  
    )
    
    
    row_data=[]
    
    
    def update_table():
        # Sort and update rows
        row_data.sort(key=lambda x: x[1], reverse=True)
        data_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(row[0])),

                    ft.DataCell(ft.Text(str(row[1])))
                ]
            ) for row in row_data
        ]
        people_container.update()
        
        
    def friend_button(e):
        print(friends_input.value)
        if Conv.from_firebase(friends_input.value)==None: 
            friends_input.helper_text="User does not exist"
            
            friends_input.helper_style=ft.TextStyle(color='#c54b4b',)
            friends_input.border_color="#c54b4b"
            
            #friends_input.hint_text="User does not exist"
            friends_input.update()
        else:
            f=friends_input.value
            friends_input.value=None
            page.close(friend_dialog)
            
            data= Conv.get_streak(f) 
            base=Conv.from_firebase("NasaKun")
            right=base.get('friends')
            
            for i in right: print("try friends",i)
            
            if data == None: data=0
            
            
            if f not in [row[0] for row in row_data ]:
                row_data.append([f, data])
                user_friends.append(str(f))
                user_data={
                'handle':user,
                'friends':user_friends
                }
                
                Conv.to_firebase(user_data)
                
            
            update_table()
        
        
    user_container=ft.Container(
        ft.Column([friends_input,ft.CupertinoButton("Add", on_click=friend_button, color='#F0AD6F')], expand=True),
        bgcolor='#ffffff',
        height=100
        
        )
        
    friend_dialog=ft.AlertDialog(
        title="Enter your friend's handle",
        title_text_style=ft.TextStyle(color="#F0AD6F", size=30),
       
        content=user_container,
        
        visible=False,
        bgcolor='white',
    )
    
    
    
    streak_ref=ft.Ref[ft.Text]()
    def add_friend(e):
        friend_dialog.visible=True
        e.control.page.overlay.append(friend_dialog)
        friend_dialog.open=True
        e.control.page.update()
        
        
        
    
    people_container=ft.Container(
        
        content=ft.Row([ft.Column([ft.Text(f"Your streak: {streak} days", size=18, ref= streak_ref),
                        ft.ElevatedButton(text="Add a friend",icon=ft.Icons.ADD_ROUNDED, height=60, on_click=add_friend, bgcolor='#ffffff', color='#F0AD6F',)], spacing=50),
                        ft.Text("Compete with your friends", size=26), 
                        ft.Column([data_table], alignment=ft.MainAxisAlignment.START)], 
                       expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        bgcolor="#ffffff",

        
        border_radius=30,
        height=300,
        
        border=ft.border.all(10, "#f9cca2"),
        margin=ft.Margin(50,30,50,30),
        padding=ft.Padding(20,20,20,20),
        expand=True
        
    )
    
    row1=ft.Row([title_container])
    
    #row2=ft.Row([planner_container,conversation_container])
    
    

    page.add(headline_row ,row1, result_row, div1, ai_line, conversation_container, people_container)

ft.app(target=main,assets_dir="assets", view=ft.WEB_BROWSER, port=8550)
