# kro composition lab

Run the [knowledge-base tutorial](../../../../knowledge/kubernetes/applications-and-tools/kro/application-lab.md) from the repository root.

- [Definition](webapp-rgd.yaml) creates the WebApp API and defines workload readiness during updates.
- [Instance](webapp.yaml) requests a server with a pinned image.
- [Controller permissions](controller-access.yaml) grant the raw installation access to the lab resource types.
- [Version pins](lab-versions.json) select tools, node image and controller manifest checksum.
- [Runner](validate-lab.py) exercises API generation, HTTP, validation, scale, recreation, image failure, recovery and deletion.
