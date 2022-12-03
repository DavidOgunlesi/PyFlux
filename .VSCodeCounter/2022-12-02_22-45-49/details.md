# Details

Date : 2022-12-02 22:45:49

Directory c:\\Users\\timid\\Desktop\\graphics\\PyFlux

Total : 70 files,  5213 codes, 867 comments, 1278 blanks, all 7358 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [example.py](/example.py) | Python | 172 | 94 | 77 | 343 |
| [requirements.txt](/requirements.txt) | pip requirements | 7 | 0 | 1 | 8 |
| [resources/shaders/basic_lit.glsl](/resources/shaders/basic_lit.glsl) | GLSL | 152 | 34 | 42 | 228 |
| [resources/shaders/env/lightmap/null_frag.glsl](/resources/shaders/env/lightmap/null_frag.glsl) | GLSL | 12 | 3 | 3 | 18 |
| [resources/shaders/env/lightmap/simpledepth_vert.glsl](/resources/shaders/env/lightmap/simpledepth_vert.glsl) | GLSL | 10 | 0 | 2 | 12 |
| [resources/shaders/env/skybox/fragment.glsl](/resources/shaders/env/skybox/fragment.glsl) | GLSL | 8 | 0 | 2 | 10 |
| [resources/shaders/env/skybox/vertex.glsl](/resources/shaders/env/skybox/vertex.glsl) | GLSL | 10 | 0 | 3 | 13 |
| [resources/shaders/env/terrainTrees/basic_lit.glsl](/resources/shaders/env/terrainTrees/basic_lit.glsl) | GLSL | 204 | 39 | 47 | 290 |
| [resources/shaders/env/terrainTrees/geom.glsl](/resources/shaders/env/terrainTrees/geom.glsl) | GLSL | 179 | 20 | 39 | 238 |
| [resources/shaders/env/terrainTrees/tess_cont.glsl](/resources/shaders/env/terrainTrees/tess_cont.glsl) | GLSL | 56 | 16 | 12 | 84 |
| [resources/shaders/env/terrainTrees/tess_eval.glsl](/resources/shaders/env/terrainTrees/tess_eval.glsl) | GLSL | 67 | 18 | 16 | 101 |
| [resources/shaders/env/terrainTrees/tess_eval_lightmap.glsl](/resources/shaders/env/terrainTrees/tess_eval_lightmap.glsl) | GLSL | 64 | 18 | 15 | 97 |
| [resources/shaders/env/terrainTrees/vert.glsl](/resources/shaders/env/terrainTrees/vert.glsl) | GLSL | 71 | 4 | 11 | 86 |
| [resources/shaders/env/terrain/basic_lit.glsl](/resources/shaders/env/terrain/basic_lit.glsl) | GLSL | 222 | 50 | 62 | 334 |
| [resources/shaders/env/terrain/geom.glsl](/resources/shaders/env/terrain/geom.glsl) | GLSL | 167 | 8 | 37 | 212 |
| [resources/shaders/env/terrain/tess_cont.glsl](/resources/shaders/env/terrain/tess_cont.glsl) | GLSL | 53 | 16 | 11 | 80 |
| [resources/shaders/env/terrain/tess_eval.glsl](/resources/shaders/env/terrain/tess_eval.glsl) | GLSL | 64 | 18 | 13 | 95 |
| [resources/shaders/env/terrain/tess_eval_lightmap.glsl](/resources/shaders/env/terrain/tess_eval_lightmap.glsl) | GLSL | 64 | 18 | 15 | 97 |
| [resources/shaders/env/terrain/vert.glsl](/resources/shaders/env/terrain/vert.glsl) | GLSL | 69 | 4 | 12 | 85 |
| [resources/shaders/env/tree/geom.glsl](/resources/shaders/env/tree/geom.glsl) | GLSL | 29 | 0 | 7 | 36 |
| [resources/shaders/env/tree/vertex.glsl](/resources/shaders/env/tree/vertex.glsl) | GLSL | 75 | 12 | 19 | 106 |
| [resources/shaders/env/water/frag.glsl](/resources/shaders/env/water/frag.glsl) | GLSL | 177 | 34 | 49 | 260 |
| [resources/shaders/env/water/tess_eval.glsl](/resources/shaders/env/water/tess_eval.glsl) | GLSL | 185 | 41 | 30 | 256 |
| [resources/shaders/env/water/tess_eval_lightmap.glsl](/resources/shaders/env/water/tess_eval_lightmap.glsl) | GLSL | 180 | 33 | 30 | 243 |
| [resources/shaders/env/water/vert.glsl](/resources/shaders/env/water/vert.glsl) | GLSL | 65 | 5 | 18 | 88 |
| [resources/shaders/fragment.glsl](/resources/shaders/fragment.glsl) | GLSL | 153 | 34 | 42 | 229 |
| [resources/shaders/misc/rendertexture/frag.glsl](/resources/shaders/misc/rendertexture/frag.glsl) | GLSL | 7 | 1 | 3 | 11 |
| [resources/shaders/misc/rendertexture/vert.glsl](/resources/shaders/misc/rendertexture/vert.glsl) | GLSL | 9 | 0 | 2 | 11 |
| [resources/shaders/postprocessing/default.glsl](/resources/shaders/postprocessing/default.glsl) | GLSL | 7 | 0 | 3 | 10 |
| [resources/shaders/postprocessing/filmgrain.glsl](/resources/shaders/postprocessing/filmgrain.glsl) | GLSL | 18 | 0 | 6 | 24 |
| [resources/shaders/postprocessing/grayscale.glsl](/resources/shaders/postprocessing/grayscale.glsl) | GLSL | 9 | 0 | 3 | 12 |
| [resources/shaders/postprocessing/inversion.glsl](/resources/shaders/postprocessing/inversion.glsl) | GLSL | 7 | 0 | 3 | 10 |
| [resources/shaders/postprocessing/volumetric/lightshaft.glsl](/resources/shaders/postprocessing/volumetric/lightshaft.glsl) | GLSL | 35 | 12 | 10 | 57 |
| [resources/shaders/preoccpass/frag.glsl](/resources/shaders/preoccpass/frag.glsl) | GLSL | 5 | 0 | 1 | 6 |
| [resources/shaders/preoccpass/vert.glsl](/resources/shaders/preoccpass/vert.glsl) | GLSL | 12 | 0 | 3 | 15 |
| [resources/shaders/sprite/unlit.glsl](/resources/shaders/sprite/unlit.glsl) | GLSL | 12 | 0 | 2 | 14 |
| [resources/shaders/unlit.glsl](/resources/shaders/unlit.glsl) | GLSL | 14 | 0 | 3 | 17 |
| [resources/shaders/uv.glsl](/resources/shaders/uv.glsl) | GLSL | 15 | 1 | 3 | 19 |
| [resources/shaders/vertex.glsl](/resources/shaders/vertex.glsl) | GLSL | 25 | 3 | 5 | 33 |
| [src/core/collections/light.py](/src/core/collections/light.py) | Python | 10 | 0 | 3 | 13 |
| [src/core/collections/mesh.py](/src/core/collections/mesh.py) | Python | 10 | 0 | 3 | 13 |
| [src/core/component.py](/src/core/component.py) | Python | 35 | 0 | 11 | 46 |
| [src/core/components/audio.py](/src/core/components/audio.py) | Python | 76 | 7 | 13 | 96 |
| [src/core/components/boid.py](/src/core/components/boid.py) | Python | 138 | 23 | 44 | 205 |
| [src/core/components/camera.py](/src/core/components/camera.py) | Python | 131 | 3 | 23 | 157 |
| [src/core/components/light.py](/src/core/components/light.py) | Python | 65 | 0 | 15 | 80 |
| [src/core/components/mesh.py](/src/core/components/mesh.py) | Python | 318 | 42 | 92 | 452 |
| [src/core/components/modelRenderer.py](/src/core/components/modelRenderer.py) | Python | 67 | 3 | 21 | 91 |
| [src/core/components/postprocessing.py](/src/core/components/postprocessing.py) | Python | 121 | 12 | 34 | 167 |
| [src/core/components/skybox.py](/src/core/components/skybox.py) | Python | 36 | 1 | 9 | 46 |
| [src/core/components/sprite.py](/src/core/components/sprite.py) | Python | 42 | 1 | 12 | 55 |
| [src/core/components/terrain.py](/src/core/components/terrain.py) | Python | 274 | 30 | 60 | 364 |
| [src/core/components/transform.py](/src/core/components/transform.py) | Python | 82 | 0 | 21 | 103 |
| [src/core/constants.py](/src/core/constants.py) | Python | 2 | 0 | 0 | 2 |
| [src/core/eventsystem.py](/src/core/eventsystem.py) | Python | 33 | 3 | 8 | 44 |
| [src/core/fileloader.py](/src/core/fileloader.py) | Python | 76 | 33 | 18 | 127 |
| [src/core/gametime.py](/src/core/gametime.py) | Python | 2 | 0 | 0 | 2 |
| [src/core/globals.py](/src/core/globals.py) | Python | 9 | 0 | 2 | 11 |
| [src/core/input.py](/src/core/input.py) | Python | 27 | 0 | 7 | 34 |
| [src/core/material.py](/src/core/material.py) | Python | 71 | 1 | 23 | 95 |
| [src/core/object.py](/src/core/object.py) | Python | 60 | 1 | 11 | 72 |
| [src/core/primitives.py](/src/core/primitives.py) | Python | 190 | 15 | 5 | 210 |
| [src/core/runtime.py](/src/core/runtime.py) | Python | 155 | 25 | 44 | 224 |
| [src/core/scene.py](/src/core/scene.py) | Python | 103 | 1 | 19 | 123 |
| [src/core/shader.py](/src/core/shader.py) | Python | 97 | 17 | 24 | 138 |
| [src/core/singleton.py](/src/core/singleton.py) | Python | 14 | 23 | 5 | 42 |
| [src/core/stdlib.py](/src/core/stdlib.py) | Python | 21 | 0 | 4 | 25 |
| [src/core/texture.py](/src/core/texture.py) | Python | 98 | 20 | 25 | 143 |
| [src/core/util.py](/src/core/util.py) | Python | 3 | 0 | 1 | 4 |
| [src/main.py](/src/main.py) | Python | 157 | 70 | 59 | 286 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)