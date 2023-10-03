from requests_html import AsyncHTMLSession

"""
        <tr>
          <td class="counter text-center">59</td>
          <td class="missionname">
            <a
              class="out"
              href="Aditya_L1.html"
              title="More details of PSLV-C57/Aditya-L1 Mission"
            >
              <span class="title"> PSLV-C57/Aditya-L1 Mission </span>
            </a>
          </td>
          <td class="LaunchDate">
            <span class="date-display-single"> Sep 02, 2023 </span>
          </td>
          <td class="launchertype">PSLV-XL</td>
          <td class="payload">
            <a
              class="out"
              title="More details about payloads of PSLV-C57/Aditya-L1 Mission"
              href="Aditya_L1_Payload.html"
              ><span class="title"> Aditya-L1 payloads </span></a
            >
          </td>
          <td class="launchremarks"></td>
        </tr>
"""

ISRO_URL = "https://www.isro.gov.in/"
PSLV_URL = ISRO_URL + "/" + "PSLV_Launchers.html"
asession = AsyncHTMLSession()


async def get_pslv():
    r = await asession.get(PSLV_URL)
    return r


response = asession.run(get_pslv)
pslv_html = response[0].html
pslv_table = pslv_html.find("table", first=True)
pslv_table_body = pslv_table.find("tbody", first=True)

with open("dataset.csv", "w") as file:
    file.write(
        "counter,mission_link,mission_title,launch_date, launch_type,payload_text,payload_link,launch_remarks\n"
    )
    pslv_tr = pslv_table_body.find("tr")
    for tr in pslv_tr:
        counter = tr.find(".counter", first=True).text
        anchor = tr.find("a", first=True)
        mission_link = ISRO_URL + anchor.attrs["href"]
        mission_title = anchor.find(".title", first=True).text
        launch_date = tr.find(".LaunchDate", first=True).text.replace(",", " ")
        launch_type = tr.find(".lauchertype", first=True) or "unknown"
        payload = tr.find(".payload", first=True) or "unknown"

        p_a = payload.find("a", first=True)
        if p_a:
            payload_text = p_a.text
            payload_link = ISRO_URL + p_a.attrs["href"]
        else:
            payload_anchor = "unknown"
            payload_link = "unknown"

        launch_remarks = tr.find(".launchremarks", first=True).text or "unknown"

        file.write(
            f"{counter},{mission_link},{mission_title},{launch_date},{launch_type},{payload_text},{payload_link},{launch_remarks}\n"
        )
