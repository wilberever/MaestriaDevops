"""
Genera pipeline_cicd_gcp.drawio  — pipeline CI/CD con Terraform + GCP Data Lake
"""
import xml.etree.ElementTree as ET

# ─── Helpers ─────────────────────────────────────────────────────────────────
_id = 0
def nid():
    global _id; _id += 1; return str(_id)

def cell(parent, cid, value, style, x, y, w, h, vertex=True, edge=False,
         src=None, tgt=None):
    c = ET.SubElement(parent, "mxCell",
        id=cid, value=value, style=style,
        vertex=("1" if vertex else "0"),
        edge=("1" if edge else "0"),
        parent="1")
    geo = ET.SubElement(c, "mxGeometry",
        x=str(x), y=str(y), width=str(w), height=str(h))
    geo.set("as", "geometry")
    if src:  c.set("source", src)
    if tgt:  c.set("target", tgt)
    return c

def edge_cell(parent, cid, src, tgt, style, value=""):
    c = ET.SubElement(parent, "mxCell",
        id=cid, value=value, style=style,
        edge="1", vertex="0",
        source=src, target=tgt, parent="1")
    geo = ET.SubElement(c, "mxGeometry", relative="1")
    geo.set("as", "geometry")
    return c

# ─── Styles ──────────────────────────────────────────────────────────────────
def s_box(fill, stroke=None, fc="white", fs=9, bold=False, align="center",
          radius=6, wrap=True, opacity=100):
    stroke = stroke or fill
    fw = "bold" if bold else "normal"
    return (f"rounded=1;arcSize=8;whiteSpace={'wrap' if wrap else 'nowrap'};"
            f"html=1;fillColor={fill};fontColor={fc};strokeColor={stroke};"
            f"fontSize={fs};fontStyle={'1' if bold else '0'};"
            f"align={align};verticalAlign=middle;opacity={opacity};")

S_TITLE   = s_box("#1A237E", bold=True, fs=17)
S_HDR_GEN = s_box("#1565C0", bold=True, fs=10)
S_HDR_SEC = s_box("#B71C1C", bold=True, fs=10)
S_HDR_INF = s_box("#1B5E20", bold=True, fs=10)
S_HDR_MON = s_box("#4A148C", bold=True, fs=10)

S_BODY_B  = s_box("#E3F2FD", "#90CAF9", fc="#0D47A1", opacity=80)
S_BODY_R  = s_box("#FFEBEE", "#EF9A9A", fc="#B71C1C", opacity=80)
S_BODY_G  = s_box("#E8F5E9", "#A5D6A7", fc="#1B5E20", opacity=80)
S_BODY_P  = s_box("#F3E5F5", "#CE93D8", fc="#4A148C", opacity=80)

S_TOOL    = s_box("#0277BD", fs=8)
S_SEC     = s_box("#C62828", fs=8)
S_INFRA   = s_box("#2E7D32", fs=8)
S_MON     = s_box("#6A1B9A", fs=8)
S_GATE    = s_box("#E65100", fs=8, bold=True)
S_ENV_D   = s_box("#455A64", bold=True, fs=8)
S_ENV_S   = s_box("#4527A0", bold=True, fs=8)
S_ENV_P   = s_box("#1B5E20", bold=True, fs=8)
S_LEGEND  = s_box("#37474F", bold=True, fs=9)
S_FOOTER  = ("text;html=1;align=center;verticalAlign=middle;resizable=0;"
             "points=[];autosize=1;strokeColor=none;fillColor=none;"
             "fontSize=8;fontColor=#78909C;fontStyle=2;")
S_LABEL   = ("text;html=1;align=left;verticalAlign=middle;resizable=0;"
             "strokeColor=none;fillColor=none;fontSize=8.5;fontColor=#263238;")
S_SECTION = ("text;html=1;align=center;verticalAlign=middle;resizable=0;"
             "strokeColor=none;fillColor=none;fontSize=8;fontColor=#546E7A;"
             "fontStyle=2;")

S_ARROW = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;"
           "jettySize=auto;exitX=1;exitY=0.5;exitDx=0;exitDy=0;"
           "entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
           "strokeColor=#37474F;strokeWidth=2.5;fillColor=#37474F;"
           "endArrow=block;endFill=1;")
S_FEEDBACK = ("edgeStyle=elbowEdgeStyle;elbow=vertical;rounded=1;"
              "exitX=0.5;exitY=1;exitDx=0;exitDy=0;"
              "entryX=0.5;entryY=1;entryDx=0;entryDy=0;"
              "strokeColor=#6A1B9A;strokeWidth=2;fillColor=#6A1B9A;"
              "endArrow=block;endFill=1;dashed=1;dashPattern=8 4;"
              "curved=1;")

# ─── Layout constants ─────────────────────────────────────────────────────────
W  = 2500   # canvas width
GAP = 12
COL_W = 365
NCOLS = 6
START_X = 30
# x positions of each column
XS = [START_X + i * (COL_W + GAP) for i in range(NCOLS)]
# last col is slightly wider
XS[5] = XS[4] + COL_W + GAP
LAST_W = W - XS[5] - 30  # ~378

TITLE_Y = 20;  TITLE_H = 65
HDR_Y   = 100; HDR_H   = 65
BODY_Y  = 175; BODY_H  = 440
ITEM_H  = 72;  ITEM_GAP = 10
ITEM_X_PAD = 12
ITEM_W = COL_W - ITEM_X_PAD * 2

ENV_Y  = 635; ENV_H = 50
FB_Y   = 700
LEG_Y  = 735; LEG_H = 60
FOOT_Y = 805

# ─── Build XML ───────────────────────────────────────────────────────────────
model = ET.Element("mxGraphModel",
    dx="1422", dy="762", grid="0", gridSize="10",
    guides="1", tooltips="1", connect="1", arrows="1",
    fold="1", page="0", pageScale="1",
    pageWidth=str(W), pageHeight="880",
    math="0", shadow="0")

root = ET.SubElement(model, "root")
ET.SubElement(root, "mxCell", id="0")
ET.SubElement(root, "mxCell", id="1", parent="0")

# ── Title ────────────────────────────────────────────────────────────────────
cell(root, nid(),
     "PIPELINE CI/CD AUTOMATIZADO CON TERRAFORM  |  Data Lake en Google Cloud Platform (GCP)",
     S_TITLE, START_X, TITLE_Y, W - START_X*2, TITLE_H)

# ─── Stage definitions ────────────────────────────────────────────────────────
stages = [
    {
        "header": "1.  Control de Versiones",
        "hs": S_HDR_GEN, "bs": S_BODY_B,
        "items": [
            (S_TOOL,  "Repositorio Git\n(GitHub)"),
            (S_TOOL,  "Pull Request + Code Review\n(CODEOWNERS obligatorio)"),
        ]
    },
    {
        "header": "2.  Integración Continua\n+ DevSecOps",
        "hs": S_HDR_SEC, "bs": S_BODY_R,
        "items": [
            (S_TOOL,  "Trigger \"pipeline-plan\"\n(push a main, automático)"),
            (S_TOOL,  "terraform fmt -check\nterraform validate"),
            (S_SEC,   "tfsec  — SAST IaC\n(CWE / CVE scan)"),
        ]
    },
    {
        "header": "3.  Terraform Plan",
        "hs": S_HDR_GEN, "bs": S_BODY_B,
        "items": [
            (S_TOOL,  "Remote Backend\nGCS Bucket + State Lock"),
            (S_INFRA, "terraform plan\n-out=tfplan.bin"),
            (S_INFRA, "Plan publicado en GCS\n(gs://tf-state-datalake/plans)"),
        ]
    },
    {
        "header": "4.  Terraform Apply\n(GCP Infra)",
        "hs": S_HDR_INF, "bs": S_BODY_G,
        "items": [
            (S_GATE,  "Trigger \"pipeline-apply\"\napproval_required = true"),
            (S_INFRA, "terraform apply tfplan.bin"),
            (S_INFRA, "Cloud Storage  — Data Lake\n(raw / processed / curated)"),
            (S_INFRA, "BigQuery  — Dataset\ndata_mart"),
            (S_SEC,   "Service Account Dataflow\n(mínimo privilegio)"),
        ]
    },
    {
        "header": "5.  Validación\ndel Servicio",
        "hs": S_HDR_GEN, "bs": S_BODY_B,
        "items": [
            (S_TOOL,  "Smoke Tests\n(gsutil / bq — Cloud SDK)"),
            (S_INFRA, "Chequeo de los 3 buckets\n+ existencia del dataset"),
        ]
    },
    {
        "header": "6.  Monitoreo\ny Control",
        "hs": S_HDR_MON, "bs": S_BODY_P,
        "items": [
            (S_MON,  "Cloud Monitoring\nAlert Policy"),
            (S_MON,  "Notificación por Email\nante errores"),
        ]
    },
]

# ── Draw stages ────────────────────────────────────────────────────────────
hdr_ids = []
for i, st in enumerate(stages):
    w = LAST_W if i == 5 else COL_W
    x = XS[i]

    # header
    hid = nid()
    hdr_ids.append(hid)
    cell(root, hid, st["header"], st["hs"], x, HDR_Y, w, HDR_H)

    # body background
    cell(root, nid(), "", st["bs"], x, BODY_Y, w, BODY_H)

    # items
    iy = BODY_Y + 14
    iw = w - ITEM_X_PAD * 2
    for style, text in st["items"]:
        cell(root, nid(), text, style,
             x + ITEM_X_PAD, iy, iw, ITEM_H)
        iy += ITEM_H + ITEM_GAP

# ── Horizontal arrows ──────────────────────────────────────────────────────
for i in range(len(stages) - 1):
    edge_cell(root, nid(), hdr_ids[i], hdr_ids[i+1], S_ARROW)

# ── Feedback loop label ────────────────────────────────────────────────────
cell(root, nid(),
     "&#8634;  Feedback Loop  —  Alertas al equipo DevOps ante fallos (sin rollback automatico todavia)",
     S_SECTION,
     START_X, FB_Y, W - START_X*2, 30)

edge_cell(root, nid(), hdr_ids[5], hdr_ids[0], S_FEEDBACK,
          "")

# ── Environment bars ───────────────────────────────────────────────────────
# Local: col 0
cell(root, nid(), "LOCAL  —  Desarrollo",
     S_ENV_D, XS[0], ENV_Y, COL_W, ENV_H)
# Staging: cols 1-2
cell(root, nid(), "STAGING  —  Cloud Build Runner",
     S_ENV_S, XS[1], ENV_Y, COL_W*2 + GAP, ENV_H)
# Prod: cols 3-5
last_end = XS[5] + LAST_W
prod_start = XS[3]
cell(root, nid(), "PRODUCCION  —  GCP Project  (IaC Managed)",
     S_ENV_P, prod_start, ENV_Y, last_end - prod_start, ENV_H)

# ── Legend ─────────────────────────────────────────────────────────────────
cell(root, nid(), "Leyenda:", S_LEGEND,
     START_X, LEG_Y, 80, 30)

legend_items = [
    (S_TOOL,  "Herramienta / Proceso"),
    (S_SEC,   "Control de Seguridad (DevSecOps)"),
    (S_INFRA, "Recurso GCP / IaC"),
    (S_MON,   "Monitoreo / Auditoria"),
    (S_GATE,  "Approval Gate (Cloud Build)"),
]
lx = START_X + 90
for (sty, lbl) in legend_items:
    cell(root, nid(), "", sty, lx, LEG_Y + 5, 22, 22)
    cell(root, nid(), lbl, S_LABEL, lx + 26, LEG_Y + 5, 200, 22)
    lx += 238

# ── Footer ─────────────────────────────────────────────────────────────────
cell(root, nid(),
     "Pipeline CI/CD Automatizado  |  Terraform IaC  |  GCP Data Lake  "
     "|  Maestria DevOps  —  2026",
     S_FOOTER,
     START_X, FOOT_Y, W - START_X*2, 30)

# ─── Write file ───────────────────────────────────────────────────────────────
tree = ET.ElementTree(model)
ET.indent(tree, space="  ")

out = "D:/Maestria/Devops/TAC_Pipeline_Terraform_GCP/pipeline_cicd_gcp.drawio"
with open(out, "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    tree.write(f, encoding="unicode", xml_declaration=False)

print(f"OK: {out}")
