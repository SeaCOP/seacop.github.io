---
title: Officers
layout: page
---

<main>
  <table data-sortable>
    <thead>
      <tr>
        <th>Serial</th>
        <th>Name</th>
        <th>Allegation Count</th>
        <th>Last Updated</th>
      </tr>
    </thead>
    <tbody>
      {% for officer in site.officers %}
        {% comment %} Hack to convert serial to string {% endcomment %}
        {% capture serial %}{{officer.serial}}{% endcapture %}
        <tr>
          <td>{{ officer.serial | escape }}</td>
          <td><a href="{{ officer.url }}">{{ site.data.roster_normalized[serial].Name | escape }}</a></td>
          <td>{{ site.data.allegations_normalized | where: "ID #", serial | size }}</td>
          <td>{{ officer.last_updated | date: '%B %d, %Y' }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/js/sortable.min.js" integrity="sha512-DEcSaL0BWApJ//v7ZfqAI04nvK+NQcUVwrrx/l1x7OJgU0Cwbq7e459NBMzLPrm8eLPzAwBtiJJS4AvLZDZ8xA==" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/css/sortable-theme-bootstrap.css" integrity="sha512-ejAo3nK8bdfwg68A9g6QYUdqnTmcGem1OX8AeVwa+dQH2v22vEwPkbZQzltTE+bjXt72iGvglAw0h+Up+fOg0g==" crossorigin="anonymous" />
