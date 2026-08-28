import { MapContainer, TileLayer, Polyline, CircleMarker, Tooltip } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import type { Section } from "@/lib/types";
import { healthHex } from "./ui-bits";

export default function RailMap({ sections }: { sections: Section[] }) {
  return (
    <MapContainer
      center={[20.5, 80.5]}
      zoom={5}
      scrollWheelZoom={false}
      style={{ height: "100%", width: "100%", borderRadius: "0.5rem" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors &copy; CARTO"
        url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
      />
      {sections.map((s) => {
        const color = healthHex(s.healthScore);
        return (
          <Polyline
            key={s.id}
            positions={[s.from, s.to]}
            pathOptions={{ color, weight: 5, opacity: 0.9 }}
          >
            <Tooltip sticky>
              <strong>{s.id}</strong> — {s.name}
              <br />
              Health {s.healthScore} · Availability {s.availability}%
              <br />
              {s.openDefects} open defects
            </Tooltip>
          </Polyline>
        );
      })}
      {sections.map((s) => (
        <CircleMarker
          key={`${s.id}-node`}
          center={s.to}
          radius={4}
          pathOptions={{
            color: healthHex(s.healthScore),
            fillColor: healthHex(s.healthScore),
            fillOpacity: 1,
          }}
        />
      ))}
    </MapContainer>
  );
}
