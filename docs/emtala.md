# EMTALA

![Image](https://quickchart.io/graphviz?format=png&graph=digraph%20G%20%7B%20rankdir%3DTB%3B%20node%20%5Bshape%3Dbox%20style%3D%22rounded%2Cfilled%22%20fillcolor%3D%22%23eef6ff%22%20color%3D%22%232b5c8a%22%20fontname%3D%22Arial%22%5D%3B%20start%20%5Blabel%3D%22Patient%20comes%20to%20ED%0A%28requests%20emergency%20care%29%22%5D%3B%20mse%20%5Blabel%3D%22MSE%0Amedical%20screening%20exam%22%5D%3B%20decision%20%5Blabel%3D%22EMC%20found%3F%0Aemergency%20medical%20condition%22%20shape%3Ddiamond%20fillcolor%3D%22%23fff4d6%22%5D%3B%20no%20%5Blabel%3D%22No%20EMC%3A%0AEMTALA%20obligation%20ends%22%5D%3B%20stabilize%20%5Blabel%3D%22Stabilize%20within%20hospital%20capability%22%5D%3B%20transfer%20%5Blabel%3D%22If%20cannot%20stabilize%3A%0Aappropriate%20transfer%22%5D%3B%20start%20-%3E%20mse%20-%3E%20decision%3B%20decision%20-%3E%20no%20%5Blabel%3D%22no%22%5D%3B%20decision%20-%3E%20stabilize%20%5Blabel%3D%22yes%22%5D%3B%20stabilize%20-%3E%20transfer%20%5Blabel%3D%22if%20needed%22%5D%3B%20%7D)

![Image](https://edrawcloudpublicus.s3.amazonaws.com/edrawimage/work/2021-11-21/1637489597/main.png)

![Image](https://www.cms.gov/sites/default/files/styles/desktop_width/public/2024-01/bannerimg_patient-rm_dr.png?itok=CYLjnIpF)

![Image](https://www.cms.gov/sites/default/files/styles/cms_circular_card_350_x_350/public/2024-01/icon-doctor-lt-bkg.png?itok=ci4R5ec-)

![Image](https://www.cms.gov/sites/default/files/styles/cms_circular_card_350_x_350/public/2024-01/icon-pregnant-lt-bkg_0.png?itok=EGMeGfIL)

![Image](https://www.cms.gov/sites/default/files/styles/cms_circular_card_350_x_350/public/2024-01/icon-patient-lt-bkg_0.png?itok=J7P37kpy)

EMTALA (Emergency Medical Treatment and Labor Act) is the federal law that says most hospital emergency departments cannot refuse to screen or stabilize someone just because they cannot pay.

Core idea:

* if a patient comes to the ED (emergency department) asking for help
* the hospital must do an MSE (medical screening exam)
* if there is an EMC (emergency medical condition), the hospital must stabilize the patient or arrange an appropriate transfer

So the sequence is:

> screen first, stabilize if emergency, transfer only if appropriate.

---

### Why it exists

EMTALA was made to prevent “patient dumping.”

Patient dumping = transferring or refusing a sick patient mainly because they are uninsured or cannot pay.

So EMTALA makes emergency care based on medical need, not wallet status.

---

### What the hospital must do

1. MSE (medical screening exam)

This means checking whether an EMC (emergency medical condition) exists.

Triage (quick sorting by urgency) is not enough by itself.

2. Stabilizing treatment

If the patient has an EMC (emergency medical condition), the hospital must treat until the patient is stable.

Stable means the condition is unlikely to materially worsen during discharge or transfer.

3. Appropriate transfer

If the hospital cannot stabilize the patient with its available staff/resources, it can transfer the patient, but the transfer must be medically appropriate.

That means:

* receiving hospital accepts the patient
* records are sent
* transport is appropriate
* benefits of transfer outweigh risks

---

### Important examples

EMC (emergency medical condition) can include:

* MI (myocardial infarction)
* stroke
* sepsis
* severe trauma
* ectopic pregnancy
* active labor
* severe psychiatric emergency

Active labor matters because the “LA” in EMTALA includes Labor Act.

---

## One-line intuition

EMTALA means the ED (emergency department) has to medically screen and stabilize emergencies before money/insurance can decide anything.

---

## Pearl

HY Step 1/ethics pearl: EMTALA does not require free lifelong care or routine outpatient care; it requires emergency screening plus stabilization or appropriate transfer for an EMC (emergency medical condition).
