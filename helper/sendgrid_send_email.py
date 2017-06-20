# using SendGrid's Python Library
import sendgrid
import os
from sendgrid.helpers.mail import *
import jinja2


def email_packing_list(user_email, recipient_email, first_name, trip_name, items, core_list):
    """Send packing list in an email."""

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(user_email)
    to_email = Email(recipient_email)
    subject = first_name + "'s Packing List for " + trip_name
    content = Content("text/html", template.render({'attrs': ['a', 'b', 'c'], 'trip_name': trip_name, 'items': items, 'core_list': core_list}))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)


template = jinja2.Template("""
<html>
<h1>{{ trip_name }}</h1>
<thead>
    <tr>
        <th>Category</th>
        <th>Item</th>
        <th>Location</th>
    </tr>
</thead>
<tbody>
{% for item in items %}
    <tr>
        <td>{{ item[3] }}</td>
        <td>{{ item[0] }}</td>
        <td>{{ item[2] }}</td>
    </tr>
{% endfor %}
{% for item in core_list %}
    <tr>
        <td>{{ item[1] }}</td>
        <td>{{ item[0] }}</td>
        <td>Core Packing List<td>
    </tr>
{% endfor %}
</tbody>  
</table>  
</html>""")

