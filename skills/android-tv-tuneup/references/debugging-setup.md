# Debugging setup helper

Use this conversational helper when the user has not confirmed debugging setup and there is no currently working, authorized ADB connection. Ask through the available user-input tool, or in chat if none is available. It is a setup question, not an extra approval for work the user already requested.

## Ask one short question

> On your TV, have you enabled USB debugging or Wireless/Network debugging under Developer options? This lets me connect to inspect it.

Suggested answers:

- Yes, it is enabled.
- No, help me turn it on.
- I'm not sure / I can't find Developer options.

Don't repeat the question if the user already answered it in the current setup flow. A confirmation from an earlier session is useful context, but today's connection status is the evidence that setup still works.

## Guide the next step

**Enabled:** Ask which option is enabled only if needed to choose the connection method. For wireless debugging, use the address/port and pairing option displayed by the TV. Keep pairing codes out of saved diagnostics. USB debugging alone does not guarantee ADB is reachable over Wi-Fi; manufacturer behavior differs.

**Disabled or unsure:** Guide the user with these common paths, noting that menu names vary by model:

1. Open Settings → Device Preferences → About, or Settings → System → About.
2. Find Build or Android TV OS build and press the remote's select button about seven times, until the developer confirmation appears. If Developer options already exists, skip this step. Let the user enter any PIN locally.
3. Return to Device Preferences or System → Developer options.
4. Look for Wireless debugging, Network debugging, or ADB debugging for a Wi-Fi connection. Some TVs expose only USB debugging; ask what options the user actually sees rather than promising that this enables network ADB.
5. Explain that debugging allows an authorized computer to control the TV and should be used on a trusted network. Have the user enable the relevant option and accept the TV's own prompt, then wait for their confirmation. Do not assume that elapsed time means it is enabled.

If no usable network-debugging option exists, explain the specific limitation. A wired ADB setup may be possible on supported models, but check the model's documented data/service port requirements before recommending a cable; don't tell the user to connect two USB host ports.

## Handle the TV's connection prompt

- For an “Allow USB debugging?” prompt, ask the user to select Allow for this computer. The label may say USB even when the connection is over the network. “Always allow” is optional, not required.
- Newer wireless debugging can require pairing first, followed by a connection to a separate port. Pairing and connection endpoints are not interchangeable.
- If `adb devices -l` reports `unauthorized`, resolve the on-screen authorization. If it reports `offline` or no device, use the field guide to check the endpoint, network and connection state. Don't claim either result proves the debugging toggle is off.
- Once ADB reports `device`, verify TV identity and proceed with the requested read-only inspection. No repeated setup questions are needed while that authorized connection remains valid.
