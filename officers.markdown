---
title: Officers
layout: page
---

<main>
  <table>
    <thead>
      <tr>
        <th>Serial</th>
        <th>Name</th>
        <th>Last Updated</th>
      </tr>
    </thead>
    {% for officer in site.officers %}
      {% comment %} Hack to convert serial to string {% endcomment %}
      {% capture serial %}{{officer.serial}}{% endcapture %}
      <tr>
        <td>{{ officer.serial | escape }}</td>
        <td><a href="{{ officer.url }}">{{ site.data.roster_normalized[serial].Name | escape }}</a></td>
        <td>{{ officer.last_updated | date: '%B %d, %Y' }}</td>
      </tr>
    {% endfor %}
  </table>
</main>
