#define CGAL_MESH_3_VERBOSE 1

#include "generate.hpp"

#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>

#include <CGAL/Mesh_triangulation_3.h>
#include <CGAL/Mesh_complex_3_in_triangulation_3.h>
#include <CGAL/Mesh_criteria_3.h>

#include <CGAL/Implicit_mesh_domain_3.h>
#include <CGAL/Mesh_domain_with_polyline_features_3.h>
#include <CGAL/make_mesh_3.h>

namespace pygalmesh {

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;

typedef CGAL::Mesh_domain_with_polyline_features_3<CGAL::Labeled_mesh_domain_3<K>> Mesh_domain;

// Triangulation
typedef CGAL::Mesh_triangulation_3<Mesh_domain>::type Tr;
typedef CGAL::Mesh_complex_3_in_triangulation_3<Tr> C3t3;

// Mesh Criteria
typedef CGAL::Mesh_criteria_3<Tr> Mesh_criteria;
typedef Mesh_criteria::Facet_criteria Facet_criteria;
typedef Mesh_criteria::Cell_criteria Cell_criteria;

// translate vector<vector<array<double, 3>> to list<vector<Point_3>>
std::list<std::vector<K::Point_3>>
translate_feature_edges(
    const std::vector<std::vector<std::array<double, 3>>> & feature_edges
    )
{
  std::list<std::vector<K::Point_3>> polylines;
  for (const auto & feature_edge: feature_edges) {
    std::vector<K::Point_3> polyline;
    for (const auto & point: feature_edge) {
      polyline.push_back(K::Point_3(point[0], point[1], point[2]));
    }
    polylines.push_back(polyline);
  }
  return polylines;
}

void
generate_mesh(
    const std::shared_ptr<pygalmesh::DomainBase> & domain,
    const std::string & outfile,
    const std::vector<std::vector<std::array<double, 3>>> & feature_edges,
    const double bounding_sphere_radius,
    const bool lloyd,
    const bool odt,
    const bool perturb,
    const bool exude,
    const double edge_size,
    const double facet_angle,
    const double facet_size,
    const double facet_distance,
    const double cell_radius_edge_ratio,
    const double cell_size,
    const bool verbose,
    const int seed
    )
{
  CGAL::get_default_random() = CGAL::Random(seed);

  const double bounding_sphere_radius2 = bounding_sphere_radius > 0 ?
    bounding_sphere_radius*bounding_sphere_radius :
    // some wiggle room
    1.01 * domain->get_bounding_sphere_squared_radius();

  // wrap domain
  const auto d = [&](K::Point_3 p) {
    return domain->eval({p.x(), p.y(), p.z()});
  };

  Mesh_domain cgal_domain = Mesh_domain::create_implicit_mesh_domain(
       d,
       K::Sphere_3(CGAL::ORIGIN, bounding_sphere_radius2)
       );

  const auto native_features = translate_feature_edges(domain->get_features());
  cgal_domain.add_features(native_features.begin(), native_features.end());

  const auto polylines = translate_feature_edges(feature_edges);
  cgal_domain.add_features(polylines.begin(), polylines.end());

  Mesh_criteria criteria(
      CGAL::parameters::edge_size=edge_size,
      CGAL::parameters::facet_angle=facet_angle,
      CGAL::parameters::facet_size=facet_size,
      CGAL::parameters::facet_distance=facet_distance,
      CGAL::parameters::cell_radius_edge_ratio=cell_radius_edge_ratio,
      CGAL::parameters::cell_size=cell_size
      );

  // Mesh generation
  if (!verbose) {
    // suppress output
    std::cerr.setstate(std::ios_base::failbit);
  }
  C3t3 c3t3 = CGAL::make_mesh_3<C3t3>(
      cgal_domain,
      criteria,
      lloyd ? CGAL::parameters::lloyd() : CGAL::parameters::no_lloyd(),
      odt ? CGAL::parameters::odt() : CGAL::parameters::no_odt(),
      perturb ? CGAL::parameters::perturb() : CGAL::parameters::no_perturb(),
      exude ? CGAL::parameters::exude() : CGAL::parameters::no_exude()
      );
  if (!verbose) {
    std::cerr.clear();
  }

  // Output
  std::ofstream medit_file(outfile);
  c3t3.output_to_medit(medit_file);
  medit_file.close();

  return;
}

void
generate_with_sizing_field(
    const std::shared_ptr<pygalmesh::DomainBase> & domain,
    const std::string & outfile,
    const std::vector<std::vector<std::array<double, 3>>> & feature_edges,
    const double bounding_sphere_radius,
    const bool lloyd,
    const bool odt,
    const bool perturb,
    const bool exude,
    const double edge_size,
    const double facet_angle,
    const double facet_size,
    const double facet_distance,
    const double cell_radius_edge_ratio,
    const std::shared_ptr<pygalmesh::SizingFieldBase> & cell_size,
    const bool verbose,
    const int seed
    )
{
  CGAL::get_default_random() = CGAL::Random(seed);

  const double bounding_sphere_radius2 = bounding_sphere_radius > 0 ?
    bounding_sphere_radius*bounding_sphere_radius :
    // some wiggle room
    1.01 * domain->get_bounding_sphere_squared_radius();

  // wrap domain
  const auto d = [&](K::Point_3 p) {
    return domain->eval({p.x(), p.y(), p.z()});
  };

  Mesh_domain cgal_domain = Mesh_domain::create_implicit_mesh_domain(
       d,
       K::Sphere_3(CGAL::ORIGIN, bounding_sphere_radius2)
       );

  // cgal_domain.detect_features();

  const auto native_features = translate_feature_edges(domain->get_features());
  cgal_domain.add_features(native_features.begin(), native_features.end());

  const auto polylines = translate_feature_edges(feature_edges);
  cgal_domain.add_features(polylines.begin(), polylines.end());

  // perhaps there's a more elegant solution here
  // see <https://github.com/CGAL/cgal/issues/4145>
  if (!verbose) {
    // suppress output
    std::cerr.setstate(std::ios_base::failbit);
  }
  if (cell_size) {
    const auto size = [&](K::Point_3 p, const int, const Mesh_domain::Index&) {
        return cell_size->eval({p.x(), p.y(), p.z()});
    };
    auto criteria = Mesh_criteria(
        CGAL::parameters::edge_size=edge_size,
        CGAL::parameters::facet_angle=facet_angle,
        CGAL::parameters::facet_size=facet_size,
        CGAL::parameters::facet_distance=facet_distance,
        CGAL::parameters::cell_radius_edge_ratio=cell_radius_edge_ratio,
        CGAL::parameters::cell_size=size
        );

    // Mesh generation
    C3t3 c3t3 = CGAL::make_mesh_3<C3t3>(
        cgal_domain,
        criteria,
        lloyd ? CGAL::parameters::lloyd() : CGAL::parameters::no_lloyd(),
        odt ? CGAL::parameters::odt() : CGAL::parameters::no_odt(),
        perturb ? CGAL::parameters::perturb() : CGAL::parameters::no_perturb(),
        exude ? CGAL::parameters::exude() : CGAL::parameters::no_exude()
        );
    if (!verbose) {
      std::cerr.clear();
    }

    // Output
    std::ofstream medit_file(outfile);
    c3t3.output_to_medit(medit_file);
    medit_file.close();
  } else {
    auto criteria = Mesh_criteria(
        CGAL::parameters::edge_size=edge_size,
        CGAL::parameters::facet_angle=facet_angle,
        CGAL::parameters::facet_size=facet_size,
        CGAL::parameters::facet_distance=facet_distance,
        CGAL::parameters::cell_radius_edge_ratio=cell_radius_edge_ratio
        );

    // Mesh generation
    C3t3 c3t3 = CGAL::make_mesh_3<C3t3>(
        cgal_domain,
        criteria,
        lloyd ? CGAL::parameters::lloyd() : CGAL::parameters::no_lloyd(),
        odt ? CGAL::parameters::odt() : CGAL::parameters::no_odt(),
        perturb ? CGAL::parameters::perturb() : CGAL::parameters::no_perturb(),
        exude ? CGAL::parameters::exude() : CGAL::parameters::no_exude()
        );
    if (!verbose) {
      std::cerr.clear();
    }

    // Output
    std::ofstream medit_file(outfile);
    c3t3.output_to_medit(medit_file);
    medit_file.close();
  }
  return;
}

} // namespace pygalmesh
