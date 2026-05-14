(function () {
  const canvas = document.querySelector('.sun-flare');
  if (!canvas) return;

  const gl =
    canvas.getContext('webgl', { alpha: true, antialias: true, premultipliedAlpha: false }) ||
    canvas.getContext('experimental-webgl', { alpha: true, antialias: true, premultipliedAlpha: false });

  if (!gl) {
    canvas.style.display = 'none';
    return;
  }

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

    float circle(vec2 uv, vec2 center, float radius, float softness) {
      float d = distance(uv, center);
      return 1.0 - smoothstep(radius, radius + softness, d);
    }

    float ray(vec2 uv, vec2 center, float angle, float width, float length) {
      vec2 p = uv - center;
      float a = atan(p.y, p.x);
      float d = length(p);
      float diff = abs(atan(sin(a - angle), cos(a - angle)));
      return (1.0 - smoothstep(width, width * 2.6, diff)) * (1.0 - smoothstep(0.0, length, d));
    }

    void main() {
      vec2 uv = gl_FragCoord.xy / u_resolution.xy;
      uv.x *= u_resolution.x / u_resolution.y;

      vec2 sun = vec2(0.82 * (u_resolution.x / u_resolution.y), 0.84);
      vec2 axis = uv - sun;
      float t = u_time * u_motion;
      float pulse = 0.88 + 0.12 * sin(t * 0.7);

      float core = circle(uv, sun, 0.055, 0.07) * 2.15;
      float halo = circle(uv, sun, 0.14, 0.32) * 0.76;
      float atmosphere = circle(uv, sun, 0.28, 0.62) * 0.24;

      float rays = 0.0;
      rays += ray(uv, sun, -2.95 + sin(t * 0.18) * 0.03, 0.02, 1.45) * 0.42;
      rays += ray(uv, sun, -2.58 + cos(t * 0.22) * 0.03, 0.016, 1.2) * 0.3;
      rays += ray(uv, sun, -2.18 + sin(t * 0.16) * 0.02, 0.014, 0.96) * 0.24;

      float flare = 0.0;
      vec2 ghostA = sun + axis * -0.34 + vec2(0.018 * sin(t * 0.35), 0.0);
      vec2 ghostB = sun + axis * -0.62 + vec2(0.0, 0.012 * cos(t * 0.28));
      vec2 ghostC = sun + axis * -0.9;
      flare += circle(uv, ghostA, 0.03, 0.045) * 0.28;
      flare += circle(uv, ghostB, 0.024, 0.038) * 0.18;
      flare += circle(uv, ghostC, 0.04, 0.065) * 0.12;

      float shimmer = 0.018 * sin((uv.x + uv.y) * 36.0 + t * 0.9);
      float intensity = max(0.0, (core + halo + atmosphere + rays + flare + shimmer) * pulse);

      vec3 warm = vec3(1.0, 0.66, 0.28);
      vec3 cream = vec3(1.0, 0.88, 0.62);
      vec3 color = mix(warm, cream, core + rays);
      float alpha = clamp(intensity, 0.0, 0.88);

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
  if (!vertexShader || !fragmentShader) return;

  const program = gl.createProgram();
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    console.warn(gl.getProgramInfoLog(program));
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
      requestAnimationFrame(render);
    }
  }

  requestAnimationFrame(render);
  window.addEventListener('resize', resize);
})();
