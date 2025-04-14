from jinja2 import Template
import os

def generate_phishing_invite_html(org_name: str, repo_name: str, sender: str, target_user: str) -> str:
    template_html = """
    <div style="background:#ffffff;background-color:#ffffff;border-radius:3px;padding:20px;border:1px solid #dddddd">
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:center;width:540px;margin:0 auto;padding:0">
          <tbody><tr align="center">
            <td style="word-break:break-word;text-align:center;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;font-size:14px;padding:0">
              <div style="padding:15px 0 10px">
                <img src="https://avatars.githubusercontent.com/{{ sender }}" width="60" height="60" style="border-radius:3px">
                <img src="https://github.githubassets.com/assets/octicon-plus-96dac899f6ef.png" height="60">
                <img src="https://avatars.githubusercontent.com/{{ target_user }}" width="60" height="60" style="border-radius:3px">
              </div>
              <h1 style="font-weight:300;font-size:24px;margin:10px 0 25px;">@{{ sender }} has invited you to collaborate on the <br><strong>{{ org_name }}/<a href="https://github.com/{{ org_name }}/{{ repo_name }}" target="_blank">{{ repo_name }}</a></strong> repository</h1>
              <hr style="background-color:#d9d9d9;height:1px;margin:20px 0;border:none">
              <p style="font-size:14px;text-align:left;">
                You can <a href="https://github.com/{{ org_name }}/{{ repo_name }}/invitations" target="_blank">accept or decline</a> this invitation.
                Visit <a href="https://github.com/{{ org_name }}/{{ repo_name }}" target="_blank">the repository</a> or <a href="https://github.com/{{ sender }}" target="_blank">@{{ sender }}</a> to learn more.
              </p>
              <p style="font-size:14px;text-align:left;">
                This invitation will expire in 7 days.
              </p>
              <div style="text-align:center;padding:20px 0 25px">
                <a href="https://github.com/{{ org_name }}/{{ repo_name }}/invitations" style="background-color:#4183c4;color:#fff;padding:6px 12px;border-radius:5px;text-decoration:none;font-weight:600;">View invitation</a>
              </div>
              <p style="font-size:13px;text-align:left;">
                <strong>Note:</strong> This invitation was intended for <strong>{{ target_user }}</strong>.
                If you were not expecting this invitation, you can ignore this email.
              </p>
              <hr style="background-color:#d9d9d9;height:1px;margin:20px 0;border:none">
              <p style="font-size:12px;text-align:left;color:#777;">
                <strong>Getting a 404 error?</strong> Make sure you’re signed in as <strong>{{ target_user }}</strong>.<br>
                <strong>Button not working?</strong> Copy and paste this link into your browser:<br>
                https://github.com/{{ org_name }}/{{ repo_name }}/invitations
              </p>
            </td>
          </tr></tbody>
        </table>
    </div>
    """
    template = Template(template_html)
    html = template.render(org_name=org_name, repo_name=repo_name, sender=sender, target_user=target_user)

    os.makedirs("outputs/phishing", exist_ok=True)
    output_path = f"outputs/phishing/{org_name}_{repo_name}_{target_user}.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
