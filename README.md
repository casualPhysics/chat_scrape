# Chatscrape 

There are quite a few APIs that allow fine-tuning on large language models like GPT-3. 
You may want to have a go 
training your own model on WhatsApp chats. 
Generally, this is a bit awkward since fine tuning typically can only be done 
on data structured in a prompt-response fashion. 
This snippet of code helps you do this!

Turn the output 
```
[09/11/2020, 12:14:48] A: Text 1
[09/11/2020, 12:15:04] A: Text 2
[09/11/2020, 12:41:26] B: Text 3
[09/11/2020, 12:41:26] A: Text 4
```

Into a csv with prompt and completion columns 

```
,prompt,completion
0,Text 1. Text 2, Text 3 
1, Text 4, NaN 
```

Fine tuning can then be performed easily on 
something like openai's data preparation api. 

```openai tools fine_tunes.prepare_data -f output.csv```

https://beta.openai.com/docs/guides/fine-tuning

### Running 

Set up a virtual environment, and then run the python script with 
the following command line arguments. 
```
virtualenv env
pip install -r requirements.txt 
source env/bin/activate 
python wa_parser.py <EXPORTED_TEXT> <PROMPTER> <RESPONDER>
```

### Examples 
Export and download the WhatsApp chat of your choice 
to a ```txt``` file. 
The start of your WhatsApp export probably looks like this, in ```chat.txt```. 

```
[07/11/2020, 11:09:28] Alice Smith: Are you ok?
[07/11/2020, 11:09:32] Bob Jones: Hey there, yes I am!
```

To parse this, use 

```
python wa_parser.py chat.txt 'Alice Smith' 'Bob Jones'
```


