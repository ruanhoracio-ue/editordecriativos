"""Recorte estilo Referência 5: foto em preto e branco, fundo removido, contorno branco grosso.

É a assinatura visual do criador que o usuário quer imitar. Três caminhos, nessa ordem:
  1. PNG/WebP que já vem com alpha  -> usa o alpha direto (melhor caso, buscar "png transparent").
  2. Foto com fundo liso            -> máscara por flood fill a partir dos cantos.
  3. Foto com fundo confuso         -> GrabCut num retângulo central (mais lento, resultado irregular).

Depois: cinza com contraste, contorno branco, sombra suave. O contorno é o que dá o
aspecto de adesivo recortado da referência.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps


def _alpha_do_fundo_liso(im_rgb, tol=26):
    """Máscara por semelhança com a cor dos cantos. Bom para fundo branco/liso."""
    a = np.asarray(im_rgb).astype(np.int16)
    h, w, _ = a.shape
    cantos = np.array([a[0, 0], a[0, w - 1], a[h - 1, 0], a[h - 1, w - 1]], dtype=np.int16)
    fundo = np.median(cantos, axis=0)
    dist = np.abs(a - fundo).sum(axis=2)
    m = (dist > tol * 3).astype(np.uint8) * 255
    return Image.fromarray(m, "L")


def _alpha_grabcut(im_rgb, margem=0.08):
    import cv2
    bgr = np.asarray(im_rgb)[:, :, ::-1].copy()
    h, w = bgr.shape[:2]
    rect = (int(w * margem), int(h * margem), int(w * (1 - 2 * margem)), int(h * (1 - 2 * margem)))
    mask = np.zeros((h, w), np.uint8)
    cv2.grabCut(bgr, mask, rect, np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64), 5, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    return Image.fromarray(m, "L")


def recortar(caminho, modo="auto", contorno=14, pb=True, contraste=1.25, tol=26):
    """Devolve RGBA com o objeto em P&B e contorno branco. `modo`: auto | alpha | liso | grabcut."""
    im = Image.open(caminho)
    alpha = None
    if modo in ("auto", "alpha") and im.mode in ("RGBA", "LA", "P"):
        conv = im.convert("RGBA")
        canal = conv.split()[3]
        if np.asarray(canal).min() < 250:            # tem transparência de verdade
            alpha = canal; im = conv.convert("RGB")
    if alpha is None:
        im = im.convert("RGB")
        if modo == "grabcut": alpha = _alpha_grabcut(im)
        else:
            alpha = _alpha_do_fundo_liso(im, tol)
            if np.asarray(alpha).mean() > 245 and modo == "auto":   # nada foi removido
                alpha = _alpha_grabcut(im)
    # limpa a borda da máscara
    alpha = alpha.filter(ImageFilter.MedianFilter(5)).filter(ImageFilter.GaussianBlur(1.2))
    alpha = alpha.point(lambda v: 255 if v > 128 else 0)

    corpo = ImageOps.autocontrast(im.convert("L"), cutoff=1) if pb else im.convert("RGB")
    if pb:
        corpo = corpo.point(lambda v: max(0, min(255, int((v - 128) * contraste + 128)))).convert("RGB")

    pad = contorno + 12
    W2, H2 = im.width + pad * 2, im.height + pad * 2
    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    # contorno: máscara dilatada preenchida de branco
    borda = Image.new("L", (W2, H2), 0); borda.paste(alpha, (pad, pad))
    borda = borda.filter(ImageFilter.MaxFilter(min(23, contorno * 2 + 1)))
    branco = Image.new("RGBA", (W2, H2), (255, 255, 255, 255)); branco.putalpha(borda)
    # sombra suave por baixo do contorno
    sombra = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    sombra.putalpha(borda.filter(ImageFilter.GaussianBlur(14)).point(lambda v: int(v * 0.55)))
    out.alpha_composite(sombra.transform(sombra.size, Image.AFFINE, (1, 0, 0, 0, 1, -10)))
    out.alpha_composite(branco)
    corpo_rgba = corpo.convert("RGBA"); corpo_rgba.putalpha(alpha)
    out.alpha_composite(corpo_rgba, (pad, pad))
    return out.crop(out.getbbox())
