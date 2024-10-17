import pika
import psycopg2

def callback(ch, method, properties, body):
    text = body.decode('utf-8').upper()[::-1]
    conn = psycopg2.connect(host="postgres", database="mydb", user="user", password="password")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages (text) VALUES (%s)", (text,))
    conn.commit()
    cursor.close()
    conn.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='text_queue')

channel.basic_consume(queue='text_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages...')
channel.start_consuming()