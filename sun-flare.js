(function () {
  const canvas = document.querySelector('.sun-flare');
  if (!canvas) return;
  const hero = canvas.closest('.hero');

  const gl =
    canvas.getContext('webgl', { alpha: true, antialias: true, premultipliedAlpha: false }) ||
    canvas.getContext('experimental-webgl', { alpha: true, antialias: true, premultipliedAlpha: false });

  if (!gl) {
    hero?.classList.add('flare-webgl-unavailable');
    return;
  }

  canvas.addEventListener('webglcontextlost', (event) => {
    event.preventDefault();
    hero?.classList.add('flare-webgl-unavailable');
    cancelAnimationFrame(frameId);
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const vertexSource = `
    attribute vec2 a_position;

    void main() {
      gl_Position = vec4(a_position, 0.0, 1.0);
    }
  `;

  const fragmentSource = `
    precision mediump float;

    uniform vec2 u_resolution;
    uniform float u_time;
    uniform float u_motion;

    vec2 aspectPoint(vec2 uv, vec2 center, float aspect) {
      return vec2((uv.x - center.x) * aspect, uv.y - center.y);
    }

    float circle(vec2 uv, vec2 center, float radius, float softness, float aspect) {
      float d = length(aspectPoint(uv, center, aspect));
      return 1.0 - smoothstep(radius, radius + softness, d);
    }

    float ray(vec2 uv, vec2 center, float angle, float width, float rayLength, float aspect) {
      vec2 p = aspectPoint(uv, center, aspect);
      float a = atan(p.y, p.x);
      float d = length(p);
      float diff = abs(atan(sin(a - angle), cos(a - angle)));
      return (1.0 - smoothstep(width, width * 2.6, diff)) * (1.0 - smoothstep(0.0, rayLength, d));
    }

    void main() {
      vec2 uv = gl_FragCoord.xy / u_resolution.xy;
      float aspect = u_resolution.x / u_resolution.y;

      vec2 sun = vec2(0.82, 0.84);
      vec2 lensAxis = vec2(0.5, 0.48) - sun;
      float t = u_time * u_motion;
      float pulse = 0.88 + 0.12 * sin(t * 0.7);

      float core = circle(uv, sun, 0.028, 0.048, aspect) * 1.38;
      float halo = circle(uv, sun, 0.082, 0.24, aspect) * 0.56;
      float atmosphere = circle(uv, sun, 0.24, 0.58, aspect) * 0.16;

      float rays = 0.0;
      rays += ray(uv, sun, -2.9 + sin(t * 0.18) * 0.025, 0.014, 1.2, aspect) * 0.24;
      rays += ray(uv, sun, -2.52 + cos(t * 0.22) * 0.025, 0.011, 0.98, aspect) * 0.17;
      rays += ray(uv, sun, -2.12 + sin(t * 0.16) * 0.018, 0.01, 0.78, aspect) * 0.12;

      float flare = 0.0;
      vec2 ghostA = sun + lensAxis * 0.44 + vec2(0.012 * sin(t * 0.35), 0.0);
      vec2 ghostB = sun + lensAxis * 0.78 + vec2(0.0, 0.01 * cos(t * 0.28));
      vec2 ghostC = sun + lensAxis * 1.08;
      flare += circle(uv, ghostA, 0.02, 0.035, aspect) * 0.11;
      flare += circle(uv, ghostB, 0.016, 0.03, aspect) * 0.075;
      flare += circle(uv, ghostC, 0.032, 0.055, aspect) * 0.05;

      float shimmer = 0.006 * sin((uv.x * aspect + uv.y) * 36.0 + t * 0.9);
      float intensity = max(0.0, (core + halo + atmosphere + rays + flare + shimmer) * pulse);

      vec3 warm = vec3(1.0, 0.66, 0.28);
      vec3 cream = vec3(1.0, 0.88, 0.62);
      vec3 color = mix(warm, cream, clamp(core + rays, 0.0, 1.0));
      float alpha = clamp(intensity, 0.0, 0.5);

      gl_FragColor = vec4(color * intensity, alpha);
    }
  `;

  function createShader(type, source) {
    const shader = gl.createShader(type);
    gl.shaderSource(shader, source);
    gl.compileShader(shader);
    if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      console.warn(gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
    }
    return shader;
  }

  const vertexShader = createShader(gl.VERTEX_SHADER, vertexSource);
  const fragmentShader = createShader(gl.FRAGMENT_SHADER, fragmentSource);
  if (!vertexShader || !fragmentShader) {
    hero?.classList.add('flare-webgl-unavailable');
    return;
  }

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.warn(gl.getProgramInfoLog(program));
    hero?.classList.add('flare-webgl-unavailable');
    return;
  }

  const positionLocation = gl.getAttribLocation(program, 'a_position');
  const resolutionLocation = gl.getUniformLocation(program, 'u_resolution');
  const timeLocation = gl.getUniformLocation(program, 'u_time');
  const motionLocation = gl.getUniformLocation(program, 'u_motion');

  const buffer = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
  gl.bufferData(
    gl.ARRAY_BUFFER,
    new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
    gl.STATIC_DRAW,
  );

  let frameId = 0;
  let isVisible = true;
  let start = performance.now();

  function resize() {
    const rect = canvas.getBoundingClientRect();
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(1, Math.floor(rect.width * dpr));
    const height = Math.max(1, Math.floor(rect.height * dpr));

    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
      gl.viewport(0, 0, width, height);
    }
  }

  function render(now) {
    if (!isVisible) return;
    resize();
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.useProgram(program);
    gl.enableVertexAttribArray(positionLocation);
    gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);
    gl.uniform2f(resolutionLocation, canvas.width, canvas.height);
    gl.uniform1f(timeLocation, (now - start) * 0.001);
    gl.uniform1f(motionLocation, reducedMotion ? 0 : 1);
    gl.drawArrays(gl.TRIANGLES, 0, 6);

    if (!reducedMotion) {
      frameId = requestAnimationFrame(render);
    }
  }

  hero?.classList.add('flare-webgl-ready');
  frameId = requestAnimationFrame(render);
  window.addEventListener('resize', resize);

  if ('IntersectionObserver' in window && hero) {
    const observer = new IntersectionObserver(([entry]) => {
      isVisible = entry.isIntersecting;
      if (isVisible && !reducedMotion) {
        start = performance.now();
        cancelAnimationFrame(frameId);
        frameId = requestAnimationFrame(render);
      } else {
        cancelAnimationFrame(frameId);
      }
    });
    observer.observe(hero);
  }
})();
