from flask import Flask, request, render_template_string
import pika

app = Flask(__name__)

html = '''
    <form method="POST" action="/">
        <input type="text" name="text" />
        <input type="submit" value="Send" />
    </form>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.queue_declare(queue='text_queue')
        channel.basic_publish(exchange='', routing_key='text_queue', body=text)
        connection.close()
        return "Message sent!"
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)