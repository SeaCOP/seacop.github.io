---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
---

<main>
  <h2 class="post-list-heading">Officers</h2>
  <table>
    <thead>
      <tr>
        <th>Serial</th>
        <th>Name</th>
        <th>Last Updated</th>
      </tr>
    </thead>
    {% for officer in site.officers %}
      <tr>
        <td>{{ officer.serial | escape }}</td>
        <td><a href="{{ officer.url }}">{{ officer.name | escape }}</a></td>
        <td>{{ officer.last_updated | date: '%B %d, %Y' }}</td>
      </tr>
    {% endfor %}
  </table>
</main>
