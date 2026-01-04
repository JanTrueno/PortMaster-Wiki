# Runtimes

PortMaster runtimes are shared engines or frameworks required for some ports to run. Sharing runtimes between ports reduces the overall size of each port, saving space on your device.

!!! info 
    Runtimes are automatically downloaded when you have an internet connection. If you have an offline device, use the options below to manually install runtimes.

## Packaged Runtimes

Packaged runtimes are complete collections of multiple runtime files bundled into a single `.zip` file. This is the easiest way to install runtimes on offline devices.

!!! info inline end "Package Types"
    - **All Runtimes**: Every available runtime for your architecture
    - **Popular Runtimes**: Most commonly needed runtimes (smaller download)
    
    Choose based on your storage capacity and needs.

{% if runtimes_zips|length == 0 %}
No packaged runtimes found.
{% else %}
{% set archs_zips = {} %}
{% for pkg in runtimes_zips %}
  {% set arch = 'aarch64' if 'aarch64' in pkg.file_name else 'x86_64' if 'x86_64' in pkg.file_name else 'unknown' %}
  {% if arch not in archs_zips %}
    {% set _ = archs_zips.update({arch: []}) %}
  {% endif %}
  {% set _ = archs_zips[arch].append(pkg) %}
{% endfor %}

=== "aarch64"

    | Package Name | Files | Updated | Size | Download |
    |--------------|-------|---------|------|:--------:|
    {% if 'aarch64' in archs_zips -%}
    {%- for pkg in archs_zips['aarch64'] -%}
    {%- set sizeMB = (pkg.size / (1024 * 1024))|round(1) if pkg.size else 'N/A' -%}
    {%- set fileCount = pkg.included_files|length if pkg.included_files else 0 -%}
    {%- set dateUpdated = pkg.date_updated if pkg.date_updated else 'N/A' -%}
    | {{ pkg.nice_name }} | {{ fileCount }} runtimes | {{ dateUpdated }} | {{ sizeMB }} MB | [Download :material-download-box:]({{ pkg.url }}){:target="_blank" rel="noopener" .md-button} |
    {% endfor -%}
    {%- else -%}
    | No packages available | | | | |
    {%- endif %}

=== "x86_64"

    | Package Name | Files | Updated | Size | Download |
    |--------------|-------|---------|------|:--------:|
    {% if 'x86_64' in archs_zips -%}
    {%- for pkg in archs_zips['x86_64'] -%}
    {%- set sizeMB = (pkg.size / (1024 * 1024))|round(1) if pkg.size else 'N/A' -%}
    {%- set fileCount = pkg.included_files|length if pkg.included_files else 0 -%}
    {%- set dateUpdated = pkg.date_updated if pkg.date_updated else 'N/A' -%}
    | {{ pkg.nice_name }} | {{ fileCount }} runtimes | {{ dateUpdated }} | {{ sizeMB }} MB | [Download :material-download-box:]({{ pkg.url }}){:target="_blank" rel="noopener" .md-button} |
    {% endfor -%}
    {%- else -%}
    | No packages available | | | | |
    {%- endif %}

{% endif %}

## How to Install

1. Download the package for your device architecture
2. Copy the `.zip` file to your autoinstall folder (see table blow)
3. Run PortMaster - it will automatically install all runtimes from the package

| CFW              | Autoinstall Folder Path            |
| ---------------- | ---------------------------------- |
| **Knulli**       | `/userdata/roms/ports/autoinstall` |
| **muOS**         | `/ports/autoinstall`          |
| **ArkOS**        | `/roms/ports/autoinstall`          |
| **ROCKNIX**      | `/roms/ports/autoinstall`          |
| **AmberElec**    | `/roms/ports/autoinstall`          |
| **UnofficialOS** | `/roms/ports/autoinstall`          |


---

## Individual Runtimes

Individual runtime files can be downloaded separately if you only need specific runtimes. These are `.squashfs` files that must be placed directly in your libs folder.

{% set utils = ports.get('utils', {}) %}
{% set archs_dict = {} %}
{% for key, entry in utils.items() %}
  {% set lowerKey = key.lower() %}
  {% if 'images' not in lowerKey and 'gameinfo' not in lowerKey %}
    {% set arch = entry.runtime_arch if entry.runtime_arch else 'unknown' %}
    {% if arch not in archs_dict %}
      {% set _ = archs_dict.update({arch: []}) %}
    {% endif %}
    {% set _ = archs_dict[arch].append((key, entry)) %}
  {% endif %}
{% endfor %}

{% if archs_dict|length == 0 %}
No individual runtimes found.
{% else %}

=== "aarch64"

    | Runtime Name | Architecture | Size | Download |
    |--------------|--------------|------|:--------:|
    {% if 'aarch64' in archs_dict -%}
    {%- for key, entry in archs_dict['aarch64'] -%}
    {%- set sizeMB = (entry.size / (1024 * 1024))|round(1) if entry.size else 'N/A' -%}
    | {{ entry.name or key }} | aarch64 | {{ sizeMB }} MB | [Download :material-download-box:]({{ entry.url }}){:target="_blank" rel="noopener" .md-button} |
    {% endfor -%}
    {%- else -%}
    | No runtimes available | | | |
    {%- endif %}

=== "armhf"

    | Runtime Name | Architecture | Size | Download |
    |--------------|--------------|------|:--------:|
    {% if 'armhf' in archs_dict -%}
    {%- for key, entry in archs_dict['armhf'] -%}
    {%- set sizeMB = (entry.size / (1024 * 1024))|round(1) if entry.size else 'N/A' -%}
    | {{ entry.name or key }} | armhf | {{ sizeMB }} MB | [Download :material-download-box:]({{ entry.url }}){:target="_blank" rel="noopener" .md-button} |
    {% endfor -%}
    {%- else -%}
    | No runtimes available | | | |
    {%- endif %}

=== "x86_64"

    | Runtime Name | Architecture | Size | Download |
    |--------------|--------------|------|:--------:|
    {% if 'x86_64' in archs_dict -%}
    {%- for key, entry in archs_dict['x86_64'] -%}
    {%- set sizeMB = (entry.size / (1024 * 1024))|round(1) if entry.size else 'N/A' -%}
    | {{ entry.name or key }} | x86_64 | {{ sizeMB }} MB | [Download :material-download-box:]({{ entry.url }}){:target="_blank" rel="noopener" .md-button} |
    {% endfor -%}
    {%- else -%}
    | No runtimes available | | | |
    {%- endif %}

{% endif %}

## How to Install

1. Download the specific runtime file you need (see tabs above for your architecture)
2. Copy the `.squashfs` file to your libs folder (see table below)
3. The runtime is now available for ports to use

| CFW | Libs Folder Path |
|-----|------------------|
| **Knulli** | `/userdata/system/.local/share/PortMaster/libs` |
| **MuOS** | `/MUOS/PortMaster/libs` |
| **ArkOS** | `/roms/tools/PortMaster/libs/` |
| **Rocknix** | `/roms/ports/PortMaster/libs/` |
| **AmberELEC** | `/roms/ports/PortMaster/libs/` |
| **uOS** | `/roms/ports/PortMaster/libs/` |