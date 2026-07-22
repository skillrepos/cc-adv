## Step 1: Start Claude Code
**What we're doing:** Launching Claude Code in interactive mode.  
**Why:** This is the primary way you'll interact with Claude for coding tasks.

**Action:** In the terminal, type:
```bash
claude
```

You'll see a welcome message and some update information.


![startup](./images/ccode179.png?raw=true "Startup")

<br><br>
---

## Step 2: Login
**What we're doing:** Running the */login* command in Claude Code.  
**Why:** We haven't authenticated yet.

**Action:** Hit *Enter* to dismiss the welcome message. In Claude Code at the prompt, type:
```
/login
```

![login](./images/ccode79.png?raw=true "login")

<br><br>


## Step 3: Authenticate Your Account
**What we're doing:** Connecting Claude Code to your Anthropic account.  
**Why:** Authentication enables full features and personalized settings.

**Action:** When prompted, follow the authentication flow:

### a. For *Select login method:*, choose option 1 - *Claude account with subscription*
<br>

![subscription](./images/ccode80.png?raw=true "Subscription")

<br><br>

### b. Claude will display a URL and code. We won't be able to open this, so just click on *Cancel*. 
<br>

![url popup](./images/ccode81.png?raw=true "URL popup")

<br><br>

### c. Back in the codespace screen, open the full URL displayed there - either by *Ctrl/Cmd+click* or by copying and pasting the URL into a browser tab.
<br>

![backup method](./images/ccode82.png?raw=true "backup method") 

<br><br>

### d. On the next screen that is shown, click on the *Authorize* button to give Claude Code authorization to use your Claude chat account.
<br>

![auth dialog](./images/ccode16.png?raw=true "auth dialog") 

<br><br>

### e. Next, you should see a screen with an authentication code. Click on the *Copy Code* link at the bottom to copy the authentication code.
<br>

![authentication code](./images/ccode18.png?raw=true "authentication code") 

<br><br>

### f. Go back to the codespace. In the area in the terminal under the URL, you should see a prompt like *Paste code here if prompted*. Click next to that and paste in the authentication code you copied in the previous step.
<br>

![Paste code](./images/ccode19.png?raw=true "Paste code") 

<br><br>

### g. After this, you should see an indication that login was successful, press *Enter* and you are ready to use Claude Code!
<br>

![successful login](./images/ccode83.png?raw=true "Successful login") 

<br><br>

## Step 4: Change the model
**What we're doing:** Running the */model* command in Claude Code.  
**Why:** Use a cheaper model since we're doing simple tasks.

**Action:** In Claude Code at the prompt, type:
```
/model
```
In the list that comes up, type "2" or use the arrow keys to move the pointer to "2" and hit *Enter*. Also use the left/right arrow keys to change the effort to *Medium effort*.

![login](./images/ccode209.png?raw=true "login")

You should see an indicator that the model was set to *Sonnet* with *medium* effort.

<br><br>

### You're now ready for the labs!

<br><br>
