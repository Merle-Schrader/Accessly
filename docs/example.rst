.. _example:

Example
============

.. code-block:: bash
    
    import accessly as av

    av.configure(
    colorblind={
        "types": ["redgreen"]
    },
    leftright={
        "position": "bottom"
    },
    legiblefont={
        "font": "Comic Sans MS"
    }
    alttext={
        "description": "Enter alt text here."
    }
    )

Plot your existing matplotlib code as normal, then accessly will overwrite the configured settings.