---
title: Officers
layout: page
---

<p>Click on any table header to sort by that column:</p>

<main>
  <table data-sortable>
    <thead>
      <tr>
        <th>Serial</th>
        <th>Name</th>
        <th>Allegation Count</th>
        <th>Gross Pay (2019)</th>
        <th>Use of Force Count</th>
        <th>Shootings</th>
	<th>Brady List</th>	
      </tr>
    </thead>
    <tbody>
      {% for officer in site.officers %}
        {% comment %} Hack to convert serial to string {% endcomment %}
        {% capture serial %}{{officer.serial}}{% endcapture %}
        <tr>
          <td>{{ officer.serial | escape }}</td>
          <td><a href="{{ officer.url }}">{{ site.data.roster_normalized[serial].OrigName | escape }}</a></td>
          <td>{{ site.data.allegations_normalized | where: "ID #", serial | size }}</td>
          {% comment %} This isn't 100% accurate, but it's 99.97% accurate so... {% endcomment %}
          <td>{{ site.data.compensation_normalized | where: "Name", site.data.roster_normalized[serial].Name | map: "Gross Pay" | first }}</td>
          <td>{{ site.data.use_of_force_normalized | where: "ID #", serial | size }}</td>
	  <td>{{ site.data.officer_involved_shootings_normalized | where: "ID #", serial | size }}</td>
  	  <td>{{ site.data.roster_normalized[serial].Brady_List }}</td>
        </tr>
      {% endfor %}
    </tbody>
  </table>
</main>

<script src="https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/js/sortable.min.js" integrity="sha512-DEcSaL0BWApJ//v7ZfqAI04nvK+NQcUVwrrx/l1x7OJgU0Cwbq7e459NBMzLPrm8eLPzAwBtiJJS4AvLZDZ8xA==" crossorigin="anonymous"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/sortable/0.8.0/css/sortable-theme-bootstrap.css" integrity="sha512-ejAo3nK8bdfwg68A9g6QYUdqnTmcGem1OX8AeVwa+dQH2v22vEwPkbZQzltTE+bjXt72iGvglAw0h+Up+fOg0g==" crossorigin="anonymous" />
